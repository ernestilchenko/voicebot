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
    Uproszczona wersja handlera do diagnostyki problemu.
    """
    try:
        # Pełne logowanie żądania
        logger.info("==== OTRZYMANO ŻĄDANIE WEBHOOK ====")
        logger.info(f"Metoda: {request.method}")
        logger.info(f"URL: {request.url}")
        logger.info(f"Nagłówki: {request.headers}")

        body_text = await request.text()
        logger.info(f"Treść żądania: {body_text}")

        # Tworzymy prostą odpowiedź TwiML bez dostępu do bazy danych
        response = VoiceResponse()
        response.say(
            "Dziękujemy za naciśnięcie przycisku. To jest test systemu powiadomień.",
            language="pl-PL",
            voice="Polly.Maja"
        )

        # Logowanie wygenerowanej odpowiedzi
        response_text = str(response)
        logger.info(f"Odpowiedź: {response_text}")

        return web.Response(content_type='text/xml', text=response_text)

    except Exception as e:
        logger.error(f"BŁĄD W HANDLERZE WEBHOOKA: {e}", exc_info=True)
        # Nawet w przypadku błędu tworzymy poprawną odpowiedź TwiML
        response = VoiceResponse()
        response.say(
            "Wystąpił błąd w systemie. Trwa diagnostyka problemu.",
            language="pl-PL",
            voice="Polly.Maja"
        )
        return web.Response(content_type='text/xml', text=str(response))


    except Exception as e:
        logger.error(f"ERROR IN WEBHOOK HANDLER: {e}", exc_info=True)
        # Даже при ошибке формируем валидный TwiML-ответ
        response = VoiceResponse()
        response.say(
            "Wystąpił błąd w systemie. Trwa diagnostyka problemu.",
            language="pl-PL",
            voice="Polly.Maja"
        )
        return web.Response(content_type='text/xml', text=str(response))

    except Exception as e:
        logger.error(f"Błąd podczas obsługi odpowiedzi głosowej: {e}", exc_info=True)
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

    # Dodatkowa trasa testowa
    app.router.add_get('/test-webhook', test_webhook)

    logger.info("Skonfigurowano trasy dla webhooków głosowych")


async def test_webhook(request):
    """
    Prosty endpoint testowy do sprawdzenia, czy routing działa prawidłowo.
    """
    logger.info("Test webhook endpoint called")
    return web.Response(text="Webhook test successful!")