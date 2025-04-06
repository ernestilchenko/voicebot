import logging
from datetime import datetime, timedelta

import pytz
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from bot.config import OPENAI_API_KEY
from bot.crew_manager import CrewManager
from webapp.database import SessionLocal
from webapp.models import User, Document

logger = logging.getLogger(__name__)


class ReminderSystem:
    """
    Klasa do zarządzania systemem przypomnień o wygasających dokumentach.
    Obsługuje przypomnienia przez Telegram, SMS i połączenia głosowe.
    Używa Crew AI do generowania spersonalizowanych wiadomości.
    """

    def __init__(self, bot: Bot, crew_manager=None):
        """
        Inicjalizacja systemu przypomnień.
        Args:
            bot (Bot): Instancja bota Telegram do wysyłania wiadomości
            crew_manager (CrewManager, optional): Instancja CrewManager do generowania wiadomości
        """
        self.bot = bot
        self.scheduler = AsyncIOScheduler()

        # Użyj przekazanego CrewManager lub stwórz nowy
        self.crew_manager = crew_manager or CrewManager(api_key=OPENAI_API_KEY)

        # Natychmiastowe sprawdzenie dokumentów przy starcie (po 5 sekundach)
        self.scheduler.add_job(
            self.check_all_documents,
            'date',
            run_date=datetime.now() + timedelta(seconds=5),
            id='check_documents_now'
        )

        # Regularne sprawdzanie dokumentów co godzinę
        self.scheduler.add_job(
            self.check_all_documents,
            'interval',
            hours=1,
            id='check_documents_hourly'
        )

        self.scheduler.start()
        logger.info("System przypomnień uruchomiony z integracją Crew AI")

    async def check_all_documents(self):
        """
        Sprawdzanie wszystkich dokumentów pod kątem terminu ważności
        i wysyłanie odpowiednich przypomnień.
        """
        logger.info("Sprawdzanie wszystkich dokumentów z użyciem Crew AI...")
        current_date = datetime.now(pytz.UTC)
        db = SessionLocal()

        try:
            # Wszystkie dokumenty z datą wygaśnięcia
            documents = db.query(Document).filter(Document.expiration_date != None).all()
            logger.info(f"Znaleziono {len(documents)} dokumentów")

            for doc in documents:
                if not doc.expiration_date:
                    continue

                # Oblicz różnicę w dniach
                expiry_date = doc.expiration_date
                days_diff = (expiry_date.date() - current_date.date()).days

                user = db.query(User).filter(User.id == doc.user_id).first()
                if not user or not user.phone_number:
                    logger.warning(f"Brak użytkownika lub numeru telefonu dla dokumentu {doc.id}")
                    continue

                logger.info(f"Dokument {doc.name}: pozostało {days_diff} dni")

                # Sprawdzenie dla Telegram (30 dni / 1 miesiąc przed)
                if days_diff == 30 and not doc.telegram_reminder_sent:
                    logger.info(f"Wysyłanie wiadomości Telegram dla dokumentu {doc.id} ({doc.name})")
                    await self.send_telegram_reminder(user.telegram_id, user.id, doc.id, doc.name, doc.expiration_date)
                    doc.telegram_reminder_sent = True

                # Sprawdzenie dla SMS (21 dni / 3 tygodnie przed)
                if days_diff == 21 and not doc.sms_reminder_sent:
                    logger.info(f"Wysyłanie SMS dla dokumentu {doc.id} ({doc.name})")
                    await self.send_sms_reminder(user.id, doc.id, user.phone_number, doc.name, doc.expiration_date)
                    doc.sms_reminder_sent = True

                # Sprawdzenie dla połączeń głosowych (14 dni / 2 tygodnie przed)
                if days_diff == 14 and not doc.call_reminder_sent:
                    logger.info(f"Wykonywanie połączenia głosowego dla dokumentu {doc.id} ({doc.name})")
                    await self.make_voice_call(user.id, doc.id, user.phone_number, doc.name, doc.expiration_date)
                    doc.call_reminder_sent = True

            # Zapisz zmiany w bazie danych
            db.commit()
            logger.info("Zakończono sprawdzanie dokumentów")
        except Exception as e:
            logger.error(f"Błąd podczas sprawdzania dokumentów: {e}")
        finally:
            db.close()

    async def schedule_document_reminders(self, user_id, document_id, expiration_date):
        """
        Planowanie przypomnień dla dokumentu.

        Args:
            user_id: ID użytkownika
            document_id: ID dokumentu
            expiration_date: Data wygaśnięcia dokumentu
        """
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            document = db.query(Document).filter(Document.id == document_id).first()

            if not user or not document:
                logger.error(f"Nie znaleziono użytkownika lub dokumentu: user_id={user_id}, document_id={document_id}")
                return

            # Obliczanie dat przypomnień
            exp_date = datetime.fromisoformat(expiration_date) if isinstance(expiration_date, str) else expiration_date
            one_month_before = exp_date - timedelta(days=30)
            three_weeks_before = exp_date - timedelta(weeks=3)
            two_weeks_before = exp_date - timedelta(weeks=2)

            # Zaplanuj wiadomość Telegram - 1 miesiąc przed
            self.scheduler.add_job(
                self.send_telegram_reminder,
                DateTrigger(run_date=one_month_before),
                args=[user.telegram_id, user_id, document_id, document.name, exp_date],
                id=f"telegram_{document_id}_{user_id}"
            )

            # Zaplanuj SMS - 3 tygodnie przed
            self.scheduler.add_job(
                self.send_sms_reminder,
                DateTrigger(run_date=three_weeks_before),
                args=[user_id, document_id, user.phone_number, document.name, exp_date],
                id=f"sms_{document_id}_{user_id}"
            )

            # Zaplanuj połączenie głosowe - 2 tygodnie przed
            self.scheduler.add_job(
                self.make_voice_call,
                DateTrigger(run_date=two_weeks_before),
                args=[user_id, document_id, user.phone_number, document.name, exp_date],
                id=f"call_{document_id}_{user_id}"
            )

            logger.info(f"Zaplanowano przypomnienia dla dokumentu {document_id} dla użytkownika {user_id}")

        finally:
            db.close()

    async def send_telegram_reminder(self, telegram_id, user_id, document_id, document_name, expiration_date):
        """
        Wysyłanie przypomnienia na Telegramie.

        Używa Crew AI do generowania spersonalizowanej wiadomości.
        """
        try:
            # Użyj Crew AI do wygenerowania spersonalizowanej wiadomości
            custom_message = await self.crew_manager.generate_custom_reminder(
                user_id, document_id, 'telegram'
            )

            if custom_message:
                message = custom_message
            else:
                # Backup w przypadku błędu
                formatted_date = expiration_date.strftime("%d.%m.%Y")
                message = (
                    f"📢 Przypomnienie: Twój dokument '{document_name}' wygaśnie za miesiąc "
                    f"({formatted_date}). Proszę zaplanować jego odnowienie."
                )

            await self.bot.send_message(telegram_id, message, parse_mode="Markdown")
            logger.info(f"Wysłano przypomnienie na Telegramie do użytkownika {telegram_id}")

            # Aktualizuj status w bazie danych
            db = SessionLocal()
            try:
                document = db.query(Document).filter(Document.id == document_id).first()
                if document:
                    document.telegram_reminder_sent = True
                    db.commit()
            finally:
                db.close()

        except Exception as e:
            logger.error(f"Nie udało się wysłać przypomnienia na Telegramie: {e}")

    async def send_sms_reminder(self, user_id, document_id, phone_number, document_name, expiration_date):
        """
        Wysyłanie przypomnienia SMS.

        Args:
            user_id: ID użytkownika
            document_id: ID dokumentu
            phone_number: Numer telefonu użytkownika
            document_name: Nazwa dokumentu
            expiration_date: Data wygaśnięcia
        """
        from twilio.rest import Client
        from bot.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

        try:
            # Użyj Crew AI do wygenerowania spersonalizowanej wiadomości SMS
            custom_message = await self.crew_manager.generate_custom_reminder(
                user_id, document_id, 'sms'
            )

            if custom_message:
                message_text = custom_message
            else:
                # Backup w przypadku błędu
                formatted_date = expiration_date.strftime("%d.%m.%Y")
                message_text = f"Przypomnienie: Twój dokument '{document_name}' wygasa dnia {formatted_date} (za 3 tygodnie)."

            logger.info(f"Próba wysłania SMS do {phone_number}: {message_text}")
            logger.info(f"Używam konta Twilio: {TWILIO_ACCOUNT_SID[:6]}...{TWILIO_ACCOUNT_SID[-4:]}")
            logger.info(f"Numer telefonu Twilio: {TWILIO_PHONE_NUMBER}")

            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=message_text,
                from_=TWILIO_PHONE_NUMBER,
                to=f'+{phone_number}'
            )
            logger.info(f"SMS wysłany do numeru {phone_number}: {message.sid}")

            # Aktualizuj status w bazie danych
            db = SessionLocal()
            try:
                document = db.query(Document).filter(Document.id == document_id).first()
                if document:
                    document.sms_reminder_sent = True
                    db.commit()
            finally:
                db.close()

            return True
        except Exception as e:
            logger.error(f"Błąd podczas wysyłania SMS: {e}")
            return False

    async def make_voice_call(self, user_id, document_id, phone_number, document_name, expiration_date):
        """
        Wykonywanie połączenia głosowego z przypomnieniem.

        Args:
            user_id: ID użytkownika
            document_id: ID dokumentu
            phone_number: Numer telefonu użytkownika
            document_name: Nazwa dokumentu
            expiration_date: Data wygaśnięcia
        """
        from twilio.rest import Client
        from twilio.twiml.voice_response import VoiceResponse
        from bot.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

        try:
            # Użyj Crew AI do wygenerowania spersonalizowanej wiadomości głosowej
            custom_message = await self.crew_manager.generate_custom_reminder(
                user_id, document_id, 'voice'
            )

            if custom_message:
                voice_text = custom_message
            else:
                # Backup w przypadku błędu
                formatted_date = expiration_date.strftime("%d.%m.%Y")
                voice_text = (
                    f"Uwaga! Ważne przypomnienie. Twój dokument {document_name} wygasa dnia {formatted_date}, "
                    f"czyli za dwa tygodnie. Proszę zaplanować jego odnowienie jak najszybciej. "
                    f"Dziękujemy za uwagę. To było automatyczne przypomnienie z systemu monitorowania dokumentów."
                )

            # Tworzymy TwiML dla odpowiedzi głosowej
            response = VoiceResponse()

            # Wiadomość o wygaśnięciu dokumentu
            response.say(
                voice_text,
                language="pl-PL",
                voice="Polly.Maja"
            )

            # Wykonywanie połączenia
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            call = client.calls.create(
                twiml=str(response),
                to=f'+{phone_number}',
                from_=TWILIO_PHONE_NUMBER
            )
            logger.info(f"Połączenie telefoniczne do {phone_number} zainicjowane: {call.sid}")

            # Aktualizujemy status w bazie danych
            db = SessionLocal()
            try:
                document = db.query(Document).filter(Document.id == document_id).first()
                if document:
                    document.call_reminder_sent = True
                    db.commit()
            finally:
                db.close()

            return call.sid
        except Exception as e:
            logger.error(f"Błąd podczas wykonywania połączenia głosowego: {e}")
            return None
