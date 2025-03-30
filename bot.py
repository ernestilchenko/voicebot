import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import TOKEN_TELEGRAM
from bot.handlers.start import router
from bot.scheduler import ReminderSystem

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


async def main():
    """
    Główna funkcja uruchamiająca bota.
    Inicjalizuje bota, system przypomnień i uruchamia nasłuchiwanie wiadomości.
    """
    bot = Bot(token=TOKEN_TELEGRAM)
    dp = Dispatcher(storage=MemoryStorage())

    # Inicjalizacja systemu przypomnień
    global reminder_system
    reminder_system = ReminderSystem(bot)

    # Poprawna rejestracja middleware
    dp.message.middleware(ReminderMiddleware(reminder_system))
    dp.callback_query.middleware(ReminderMiddleware(reminder_system))

    dp.include_routers(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    """
    Punkt wejścia programu.
    Konfiguruje logowanie i uruchamia główną funkcję aplikacji.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Ciche zakończenie programu przy przerwaniu przez użytkownika lub wyjściu systemowym
        pass