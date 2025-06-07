import logging
from datetime import datetime, timedelta

import pytz
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from bot.config import OPENAI_API_KEY
from bot.crew_manager import CrewManager
from webapp.models import UserProfile, Document, VoiceCall

logger = logging.getLogger(__name__)


class ReminderSystem:
    def __init__(self, bot: Bot, crew_manager=None):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.crew_manager = crew_manager or CrewManager(api_key=OPENAI_API_KEY)

        self.scheduler.add_job(
            self.check_all_documents,
            'date',
            run_date=datetime.now() + timedelta(seconds=5),
            id='check_documents_now'
        )

        self.scheduler.add_job(
            self.check_all_documents,
            'interval',
            hours=1,
            id='check_documents_hourly'
        )

        self.scheduler.start()
        logger.info("System przypomnień uruchomiony z integracją Crew AI")

    async def check_all_documents(self):
        logger.info("Sprawdzanie wszystkich dokumentów z użyciem Crew AI...")
        current_date = datetime.now(pytz.UTC)

        try:
            documents = Document.get_expiring_documents()
            logger.info(f"Znaleziono {len(documents)} dokumentów")

            for doc in documents:
                if not doc.expiration_date:
                    continue

                days_diff = (doc.expiration_date.date() - current_date.date()).days
                user = UserProfile.get_by_id(doc.user_id)

                if not user or not user.phone:
                    logger.warning(f"Brak użytkownika lub numeru telefonu dla dokumentu {doc.id}")
                    continue

                logger.info(f"Dokument {doc.title}: pozostało {days_diff} dni")

                if days_diff == 30 and not doc.telegram_reminder_sent:
                    logger.info(f"Wysyłanie wiadomości Telegram dla dokumentu {doc.id} ({doc.title})")
                    await self.send_telegram_reminder(user.telegram_id, user.id, doc.id, doc.title, doc.expiration_date)
                    doc.update_telegram_reminder_sent(True)

                if days_diff == 21 and not doc.sms_reminder_sent:
                    logger.info(f"Wysyłanie SMS dla dokumentu {doc.id} ({doc.title})")
                    await self.send_sms_reminder(user.id, doc.id, user.phone, doc.title, doc.expiration_date)
                    doc.update_sms_reminder_sent(True)

                if days_diff == 14 and not doc.call_reminder_sent:
                    if doc.call_attempts == 0 or not doc.call_message_listened:
                        retry_needed = True
                        if doc.call_attempts > 0 and doc.last_call_date:
                            from bot.config import CALL_RETRY_DAYS
                            days_since_last_call = (current_date - doc.last_call_date).days
                            retry_needed = days_since_last_call >= CALL_RETRY_DAYS

                        if retry_needed:
                            logger.info(
                                f"Wykonywanie połączenia głosowego dla dokumentu {doc.id} ({doc.title}) - próba {doc.call_attempts + 1}")
                            await self.make_voice_call(user.id, doc.id, user.phone, doc.title, doc.expiration_date)

            logger.info("Zakończono sprawdzanie dokumentów")
        except Exception as e:
            logger.error(f"Błąd podczas sprawdzania dokumentów: {e}")

    async def schedule_document_reminders(self, user_id, document_id, expiration_date):
        try:
            user = UserProfile.get_by_id(user_id)
            document = Document.get_by_id(document_id)

            if not user or not document:
                logger.error(f"Nie znaleziono użytkownika lub dokumentu: user_id={user_id}, document_id={document_id}")
                return

            exp_date = datetime.fromisoformat(expiration_date) if isinstance(expiration_date, str) else expiration_date
            one_month_before = exp_date - timedelta(days=30)
            three_weeks_before = exp_date - timedelta(weeks=3)
            two_weeks_before = exp_date - timedelta(weeks=2)

            self.scheduler.add_job(
                self.send_telegram_reminder,
                DateTrigger(run_date=one_month_before),
                args=[user.telegram_id, user_id, document_id, document.title, exp_date],
                id=f"telegram_{document_id}_{user_id}"
            )

            self.scheduler.add_job(
                self.send_sms_reminder,
                DateTrigger(run_date=three_weeks_before),
                args=[user_id, document_id, user.phone, document.title, exp_date],
                id=f"sms_{document_id}_{user_id}"
            )

            self.scheduler.add_job(
                self.make_voice_call,
                DateTrigger(run_date=two_weeks_before),
                args=[user_id, document_id, user.phone, document.title, exp_date],
                id=f"call_{document_id}_{user_id}"
            )

            logger.info(f"Zaplanowano przypomnienia dla dokumentu {document_id} dla użytkownika {user_id}")

        except Exception as e:
            logger.error(f"Błąd podczas planowania przypomnień: {e}")

    async def send_telegram_reminder(self, telegram_id, user_id, document_id, document_name, expiration_date):
        try:
            custom_message = await self.crew_manager.generate_custom_reminder(
                user_id, document_id, 'telegram'
            )

            if custom_message:
                message = custom_message
            else:
                formatted_date = expiration_date.strftime("%d.%m.%Y")
                message = (
                    f"📢 Przypomnienie: Twój dokument '{document_name}' wygaśnie za miesiąc "
                    f"({formatted_date}). Proszę zaplanować jego odnowienie."
                )

            await self.bot.send_message(telegram_id, message, parse_mode="Markdown")
            logger.info(f"Wysłano przypomnienie na Telegramie do użytkownika {telegram_id}")

            document = Document.get_by_id(document_id)
            if document:
                document.update_telegram_reminder_sent(True)

        except Exception as e:
            logger.error(f"Nie udało się wysłać przypomnienia na Telegramie: {e}")

    async def send_sms_reminder(self, user_id, document_id, phone_number, document_name, expiration_date):
        from twilio.rest import Client
        from bot.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

        try:
            custom_message = await self.crew_manager.generate_custom_reminder(
                user_id, document_id, 'sms'
            )

            if custom_message:
                message_text = custom_message
            else:
                formatted_date = expiration_date.strftime("%d.%m.%Y")
                message_text = f"Przypomnienie: Twój dokument '{document_name}' wygasa dnia {formatted_date} (za 3 tygodnie)."

            logger.info(f"Próba wysłania SMS do {phone_number}: {message_text}")

            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=message_text,
                from_=TWILIO_PHONE_NUMBER,
                to=f'+{phone_number}'
            )
            logger.info(f"SMS wysłany do numeru {phone_number}: {message.sid}")

            document = Document.get_by_id(document_id)
            if document:
                document.update_sms_reminder_sent(True)

            return True
        except Exception as e:
            logger.error(f"Błąd podczas wysyłania SMS: {e}")
            return False

    async def make_voice_call(self, user_id, document_id, phone_number, document_name, expiration_date):
        from twilio.rest import Client
        from twilio.twiml.voice_response import VoiceResponse
        from bot.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, COMPANY_NAME

        try:
            document = Document.get_by_id(document_id)
            if not document:
                logger.error(f"Nie znaleziono dokumentu: {document_id}")
                return None

            document.increment_call_attempts()
            call_attempt = document.call_attempts

            custom_message = await self.crew_manager.generate_custom_reminder(
                user_id, document_id, 'voice'
            )

            if custom_message:
                voice_text = custom_message
            else:
                formatted_date = expiration_date.strftime("%d.%m.%Y")
                voice_text = (
                    f"Twój dokument {document_name} wygasa dnia {formatted_date}, "
                    f"czyli za dwa tygodnie. Prosimy zaplanować jego odnowienie jak najszybciej."
                )

            response = VoiceResponse()
            greeting_text = f"Dzień dobry. Tutaj automatyczny system powiadomień firmy {COMPANY_NAME}. "

            if call_attempt > 1:
                greeting_text += f"To jest {call_attempt} próba kontaktu w sprawie ważnego przypomnienia. "

            full_message = greeting_text + voice_text + " Dziękujemy za uwagę."
            response.say(full_message, language="pl-PL", voice="Polly.Maja")

            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            call = client.calls.create(
                twiml=str(response),
                to=f'+{phone_number}',
                from_=TWILIO_PHONE_NUMBER
            )

            logger.info(f"Połączenie głosowe bez interaktywności do numeru {phone_number} zainicjowane: {call.sid}")

            document.update_call_message_listened(True)
            document.update_call_reminder_sent(True)

            VoiceCall.create(
                sid=call.sid,
                to_number=phone_number,
                from_number=TWILIO_PHONE_NUMBER,
                message_text=full_message,
                document_id=document_id,
                user_profile_id=user_id
            )

            return call.sid
        except Exception as e:
            logger.error(f"Błąd podczas wykonywania połączenia głosowego: {e}")
            return None
