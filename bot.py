import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot.voice_webhook import setup_voice_routes
from bot.config import TOKEN_TELEGRAM, OPENAI_API_KEY
from bot.crew_manager import CrewManager
from bot.handlers.start import router
from bot.scheduler import ReminderSystem

# Webhook settings
BASE_WEBHOOK_URL = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = f"/webhook/{TOKEN_TELEGRAM}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = int(os.getenv("PORT", 8080))

# Tworzenie globalnych zmiennych
reminder_system = None
crew_manager = None  # Dodaj globalną zmienną


# Middleware do przekazywania systemów do obsługi zdarzeń
class AppMiddleware:
    """
    Middleware dodający systemy do kontekstu obsługi zdarzeń.
    """

    def __init__(self, reminder_system, crew_manager):
        """
        Inicjalizacja middleware z systemami.
        """
        self.reminder_system = reminder_system
        self.crew_manager = crew_manager

    async def __call__(self, handler, event, data):
        """
        Wywołanie middleware przed obsługą zdarzenia.
        """
        # Dodanie systemów do danych kontekstowych
        data["reminder_system"] = self.reminder_system
        data["crew_manager"] = self.crew_manager
        return await handler(event, data)


async def on_startup(bot: Bot, dispatcher: Dispatcher):
    """
    Funkcja wywoływana podczas uruchamiania bota.
    Inicjalizuje systemy i ustawia webhook.
    """
    # Inicjalizacja systemów
    global reminder_system, crew_manager

    # Inicjalizacja CrewManager z przekazaniem klucza API OpenAI
    crew_manager = CrewManager(api_key=OPENAI_API_KEY)
    logging.info("Zainicjalizowano CrewManager z obsługą Crew AI")

    # Inicjalizacja systemu przypomnień z przekazaniem bota i CrewManager
    reminder_system = ReminderSystem(bot=bot, crew_manager=crew_manager)
    logging.info("Zainicjalizowano ReminderSystem z integracją Crew AI")

    # Rejestracja middleware
    middleware = AppMiddleware(reminder_system, crew_manager)
    dispatcher.message.middleware(middleware)
    dispatcher.callback_query.middleware(middleware)

    # Ustawienie webhooka
    await bot.set_webhook(url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
    logging.info(f"Bot started. Webhook set to: {WEBHOOK_URL}")


async def on_shutdown(bot: Bot):
    """
    Funkcja wywoływana podczas zatrzymywania bota.
    Usuwa webhook i zamyka sesję bota.
    """
    logging.info("Bot stopping. Removing webhook...")
    await bot.delete_webhook()
    await bot.session.close()


def main():
    """
    Główna funkcja uruchamiająca bota z obsługą webhooka.
    """
    # Konfiguracja logowania
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Inicjalizacja bota i dispatchera
    bot = Bot(token=TOKEN_TELEGRAM)
    dp = Dispatcher(storage=MemoryStorage())

    # Rejestracja handlera
    dp.include_router(router)

    # Rejestracja funkcji uruchamiania i zatrzymywania
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Tworzenie aplikacji aiohttp
    app = web.Application()

    # Utworzenie handlera webhooka
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )

    # Rejestracja handlera webhooka w aplikacji
    webhook_handler.register(app, path=WEBHOOK_PATH)

    # Podłączenie dispatchera do aplikacji
    setup_application(app, dp, bot=bot)

    # Konfiguracja tras dla webhooków głosowych
    setup_voice_routes(app)

    # Uruchomienie serwera webowego
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    """
    Punkt wejścia programu.
    """
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        # Ciche zakończenie programu przy przerwaniu przez użytkownika lub wyjściu systemowym
        logging.info("Bot stopped")
