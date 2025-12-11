# bot/dispatcher.py
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from db.database import Database
from config import Config
from bot.handlers import register_handlers
from bot.scheduler import start_scheduler


async def start_bot_polling():
    """
    Запускает управляющего бота (через которого добавляются каналы)
    """
    if not Config.APP_BOT_TOKEN:
        print("APP_BOT_TOKEN не установлен — управляющий бот отключён")
        return

    # Правильный способ для Aiogram 3.7.0+
    bot = Bot(
        token=Config.APP_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    db = Database(encryption_key=Config.ENCRYPT_KEY)
    db.init_db()

    # Регистрируем обработчики
    register_handlers(dp, db)

    # Запускаем планировщик публикаций
    await start_scheduler(db)

    print("Управляющий бот запущен и слушает команды...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())