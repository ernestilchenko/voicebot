import logging
import pytz
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from aiogram import Bot

from webapp.database import SessionLocal
from webapp.models import User, Document

# To będzie zaimportowane z pliku modeli po dodaniu pola
# Zakładając, że dodasz pole expiration_date do modelu Document

logger = logging.getLogger(__name__)


class ReminderSystem:
    """
    Klasa do zarządzania systemem przypomnień o wygasających dokumentach.
    Obsługuje przypomnienia przez Telegram, SMS i połączenia głosowe.
    """

    def __init__(self, bot: Bot):
        """
        Inicjalizacja systemu przypomnień.
        Args:
            bot (Bot): Instancja bota Telegram do wysyłania wiadomości
        """
        self.bot = bot
        self.scheduler = AsyncIOScheduler()

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
        logger.info("System przypomnień uruchomiony")

    async def check_all_documents(self):
        """
        Sprawdzanie wszystkich dokumentów pod kątem terminu ważności
        i wysyłanie odpowiednich przypomnień.
        """
        logger.info("Sprawdzanie wszystkich dokumentów...")
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

                # Sprawdzenie dla SMS (21 dni / 3 tygodnie przed)
                if days_diff == 21 and not doc.sms_reminder_sent:
                    logger.info(f"Wysyłanie SMS dla dokumentu {doc.id} ({doc.name})")
                    await self.send_sms_reminder(user.phone_number, doc.name, doc.expiration_date)
                    doc.sms_reminder_sent = True

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
                args=[user.telegram_id, document.name, exp_date],
                id=f"telegram_{document_id}_{user_id}"
            )

            # Zaplanuj SMS - 3 tygodnie przed
            self.scheduler.add_job(
                self.send_sms_reminder,
                DateTrigger(run_date=three_weeks_before),
                args=[user.phone_number, document.name, exp_date],
                id=f"sms_{document_id}_{user_id}"
            )

            # Zaplanuj połączenie głosowe - 2 tygodnie przed
            self.scheduler.add_job(
                self.make_voice_call,
                DateTrigger(run_date=two_weeks_before),
                args=[user.phone_number, document.name, exp_date],
                id=f"call_{document_id}_{user_id}"
            )

            logger.info(f"Zaplanowano przypomnienia dla dokumentu {document_id} dla użytkownika {user_id}")

        finally:
            db.close()

    async def send_telegram_reminder(self, telegram_id, document_name, expiration_date):
        """
        Wysyłanie przypomnienia na Telegramie.

        Args:
            telegram_id: ID użytkownika na Telegramie
            document_name: Nazwa dokumentu
            expiration_date: Data wygaśnięcia
        """
        formatted_date = expiration_date.strftime("%d.%m.%Y")
        message = (
            f"📢 Przypomnienie: Twój dokument '{document_name}' wygaśnie za miesiąc "
            f"({formatted_date}). Proszę zaplanować jego odnowienie."
        )
        try:
            await self.bot.send_message(telegram_id, message)
            logger.info(f"Wysłano przypomnienie na Telegramie do użytkownika {telegram_id}")
        except Exception as e:
            logger.error(f"Nie udało się wysłać przypomnienia na Telegramie: {e}")

    async def send_sms_reminder(self, phone_number, document_name, expiration_date):
        """
        Wysyłanie przypomnienia SMS.

        Args:
            phone_number: Numer telefonu użytkownika
            document_name: Nazwa dokumentu
            expiration_date: Data wygaśnięcia
        """
        from twilio.rest import Client
        from bot.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

        formatted_date = expiration_date.strftime("%d.%m.%Y")
        message_text = f"Przypomnienie: Twój dokument '{document_name}' wygasa dnia {formatted_date} (za 3 tygodnie)."

        logger.info(f"Próba wysłania SMS do {phone_number}: {message_text}")
        logger.info(f"Używam konta Twilio: {TWILIO_ACCOUNT_SID[:6]}...{TWILIO_ACCOUNT_SID[-4:]}")
        logger.info(f"Numer telefonu Twilio: {TWILIO_PHONE_NUMBER}")

        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=message_text,
                from_=TWILIO_PHONE_NUMBER,
                to=f'+{phone_number}'
            )
            logger.info(f"SMS wysłany do numeru {phone_number}: {message.sid}")
            return True
        except Exception as e:
            logger.error(f"Błąd podczas wysyłania SMS: {e}")
            return False

    async def make_voice_call(self, phone_number, document_name, expiration_date):
        """
        Wykonywanie połączenia głosowego z przypomnieniem.

        Args:
            phone_number: Numer telefonu użytkownika
            document_name: Nazwa dokumentu
            expiration_date: Data wygaśnięcia
        """
        # W rzeczywistej implementacji, użyłbyś API połączeń głosowych
        # To jest tylko zastępczy kod dla implementacji
        formatted_date = expiration_date.strftime("%d.%m.%Y")
        message = f"Połączenie głosowe do {phone_number}: Twój dokument wygasa dnia {formatted_date} (za 2 tygodnie)."
        logger.info(message)

        # Przykład z użyciem Twilio (potrzebujesz dodać bibliotekę Twilio i dane uwierzytelniające)
        """
        from twilio.rest import Client

        account_sid = 'twoje_account_sid'
        auth_token = 'twoj_auth_token'
        client = Client(account_sid, auth_token)

        call = client.calls.create(
            url='http://twoj-serwer.com/voice-response.xml',  # URL do TwiML z wiadomością
            to=f'+{phone_number}',
            from_='+1234567890'  # Twój numer Twilio
        )
        """