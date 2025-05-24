import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from src.database.database import init_db, async_session
from src.handlers.common import router
BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
async def set_bot_commands(bot: Bot):
    """Установка команд бота"""
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="register", description="Регистрация в системе"),
        BotCommand(command="enter_scores", description="Ввод баллов ЕГЭ"),
        BotCommand(command="view_scores", description="Просмотр моих баллов"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """Главная функция запуска бота"""
    await init_db()
    logger.info("База данных инициализирована")
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()
    @dp.message.middleware()
    @dp.callback_query.middleware()
    async def db_session_middleware(handler, event, data):
        async with async_session() as session:
            data['session'] = session
            return await handler(event, data)
    dp.include_router(router)
    await set_bot_commands(bot)
    logger.info("Бот запущен")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
if __name__ == "__main__":
    asyncio.run(main())