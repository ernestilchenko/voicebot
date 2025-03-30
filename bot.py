import asyncio
import logging
import os
from aiohttp import web

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from bot.config import TOKEN_TELEGRAM
from bot.handlers.start import router
from bot.scheduler import ReminderSystem

# Webhook settings
BASE_WEBHOOK_URL = os.getenv('WEBHOOK_HOST', 'https://voicebot-production-1898.up.railway.app')  # Replace with your Railway domain
WEBHOOK_PATH = f"/webhook/{TOKEN_TELEGRAM}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your-secret-token')  # Optional but recommended for security

# Web server settings - Railway assigns PORT env var automatically
WEB_SERVER_HOST = "0.0.0.0"  # Listen on all interfaces in container
WEB_SERVER_PORT = int(os.getenv("PORT", 8080))

# Tworzenie globalnej zmiennej dla systemu przypomnień
reminder_system = None


# Middleware do przekazywania systemu przypomnień do obsługi zdarzeń
class ReminderMiddleware:
    """
    Middleware dodający system przypomnień do kontekstu obsługi zdarzeń.
    Pozwala na dostęp do systemu przypomnień wewnątrz obsługi wiadomości i callback query.
    """

    def __init__(self, reminder_system):
        """
        Inicjalizacja middleware z systemem przypomnień.

        Args:
            reminder_system: Instancja systemu przypomnień
        """
        self.reminder_system = reminder_system

    async def __call__(self, handler, event, data):
        """
        Wywołanie middleware przed obsługą zdarzenia.

        Args:
            handler: Funkcja obsługi zdarzenia
            event: Obsługiwane zdarzenie
            data: Dane kontekstowe

        Returns:
            Wynik obsługi zdarzenia
        """
        # Dodanie reminder_system do danych, które zostaną przekazane do obsługi zdarzeń
        data["reminder_system"] = self.reminder_system

        # Również dodajemy reminder_system do Bot.data dla dostępu z callback_query
        if hasattr(event, 'bot') and hasattr(event.bot, 'data'):
            event.bot.data = getattr(event.bot, 'data', {})
            event.bot.data["reminder_system"] = self.reminder_system

        return await handler(event, data)


async def on_startup(bot: Bot, dispatcher: Dispatcher):
    """
    Funkcja wywoływana podczas uruchamiania bota.
    Inicjalizuje system przypomnień i ustawia webhook.
    """
    # Inicjalizacja systemu przypomnień
    global reminder_system
    reminder_system = ReminderSystem(bot)

    # Poprawna rejestracja middleware
    dispatcher.message.middleware(ReminderMiddleware(reminder_system))
    dispatcher.callback_query.middleware(ReminderMiddleware(reminder_system))

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