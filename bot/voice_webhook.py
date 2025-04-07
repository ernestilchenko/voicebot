import logging
from datetime import datetime

import pytz
from aiohttp import web
from twilio.twiml.voice_response import VoiceResponse

from bot.config import COMPANY_NAME
from webapp.database import SessionLocal
from webapp.models import Document, User

logger = logging.getLogger(__name__)


async def handle_voice_response(request):
    """
    Obsługuje odpowiedź użytkownika podczas połączenia głosowego.
    Sprawdza, czy użytkownik nacisnął '1', aby odsłuchać wiadomość.
    """
    try:
        # Pobieramy parametry z żądania
        params = await request.post()
        digits_pressed = params.get('Digits', '')

        # Pobieramy ID dokumentu i użytkownika z parametrów URL
        query_params = request.query
        document_id = query_params.get('document_id')
        user_id = query_params.get('user_id')

        if not document_id or not user_id:
            logger.error("Brak document_id lub user_id w żądaniu")
            return web.Response(text="Parametry nieprawidłowe", status=400)

        # Tworzymy odpowiedź głosową
        response = VoiceResponse()

        # Sprawdzamy, czy użytkownik nacisnął '1'
        if digits_pressed == '1':
            # Użytkownik potwierdził chęć odsłuchania wiadomości

            # Pobieramy dokument i użytkownika z bazy danych
            db = SessionLocal()
            try:
                document = db.query(Document).filter(Document.id == document_id).first()
                user = db.query(User).filter(User.id == user_id).first()

                if not document or not user:
                    logger.error(
                        f"Nie znaleziono dokumentu lub użytkownika: document_id={document_id}, user_id={user_id}")
                    response.say(
                        "Przepraszamy, wystąpił błąd. Prosimy o kontakt z administratorem systemu.",
                        language="pl-PL",
                        voice="Polly.Maja"
                    )
                    return web.Response(content_type='text/xml', text=str(response))

                # Możemy użyć CrewManager do wygenerowania wiadomości, ale teraz użyjemy prostej
                formatted_date = document.expiration_date.strftime(
                    "%d.%m.%Y") if document.expiration_date else "nieznana data"

                message = (
                    f"Ważne przypomnienie od firmy {COMPANY_NAME}. "
                    f"Twój dokument {document.name} wygasa w dniu {formatted_date}. "
                    f"Prosimy o zaplanowanie jego odnowienia jak najszybciej. "
                    f"Dziękujemy za uwagę."
                )

                # Odtwarzamy wiadomość
                response.say(message, language="pl-PL", voice="Polly.Maja")

                # Oznaczamy dokument jako odsłuchany
                document.call_message_listened = True
                document.call_reminder_sent = True
                db.commit()

                logger.info(f"Użytkownik {user_id} odsłuchał wiadomość o dokumencie {document_id}")
            finally:
                db.close()
        else:
            # Użytkownik nie nacisnął '1' lub nacisnął inny klawisz
            response.say(
                "Nieprawidłowy klawisz. Aby odsłuchać ważną wiadomość, naciśnij 1.",
                language="pl-PL",
                voice="Polly.Maja"
            )

            # Dajemy użytkownikowi jeszcze jedną szansę
            gather = response.gather(
                num_digits=1,
                action=f"/voice-response?document_id={document_id}&user_id={user_id}",
                method="POST"
            )
            gather.say("Naciśnij 1, aby kontynuować.", language="pl-PL", voice="Polly.Maja")

        return web.Response(content_type='text/xml', text=str(response))

    except Exception as e:
        logger.error(f"Błąd podczas obsługi odpowiedzi głosowej: {e}")
        response = VoiceResponse()
        response.say(
            "Przepraszamy, wystąpił błąd w systemie. Prosimy spróbować później.",
            language="pl-PL",
            voice="Polly.Maja"
        )
        return web.Response(content_type='text/xml', text=str(response))


async def handle_call_status(request):
    """
    Obsługuje zwrotny status połączenia z Twilio.
    """
    try:
        params = await request.post()
        call_sid = params.get('CallSid')
        call_status = params.get('CallStatus')

        logger.info(f"Status połączenia {call_sid}: {call_status}")

        return web.Response(text="OK")
    except Exception as e:
        logger.error(f"Błąd podczas obsługi statusu połączenia: {e}")
        return web.Response(text="Error", status=500)


def setup_voice_routes(app):
    """
    Konfiguruje trasy dla webhooków głosowych.
    """
    app.router.add_post('/voice-response', handle_voice_response)
    app.router.add_post('/call-status', handle_call_status)

    logger.info("Skonfigurowano trasy dla webhooków głosowych")