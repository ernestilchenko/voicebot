import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import TOKEN_TELEGRAM, OPENAI_API_KEY
from bot.crew_manager import CrewManager
from bot.handlers.start import router
from bot.scheduler import ReminderSystem

reminder_system = None
crew_manager = None


class AppMiddleware:
    def __init__(self, reminder_system, crew_manager):
        self.reminder_system = reminder_system
        self.crew_manager = crew_manager

    async def __call__(self, handler, event, data):
        data["reminder_system"] = self.reminder_system
        data["crew_manager"] = self.crew_manager
        return await handler(event, data)


async def on_startup(bot: Bot, dispatcher: Dispatcher):
    global reminder_system, crew_manager

    crew_manager = CrewManager(api_key=OPENAI_API_KEY)
    logging.info("Zainicjalizowano CrewManager z obsługą Crew AI")

    reminder_system = ReminderSystem(bot=bot, crew_manager=crew_manager)
    logging.info("Zainicjalizowano ReminderSystem z integracją Crew AI")

    middleware = AppMiddleware(reminder_system, crew_manager)
    dispatcher.message.middleware(middleware)
    dispatcher.callback_query.middleware(middleware)

    logging.info("Bot started with polling")


async def on_shutdown(bot: Bot):
    logging.info("Bot stopping...")
    await bot.session.close()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(token=TOKEN_TELEGRAM)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")