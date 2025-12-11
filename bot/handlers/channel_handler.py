# bot/handlers/channel_handler.py
# Обработчики для управления каналами

from aiogram import types
from aiogram.dispatcher import Dispatcher
from db.database import Database
from bot.validators import validate_channel

async def add_channel_handler(message: types.Message, db: Database, bot_manager):
    """
    Добавление канала через команду: /add_channel <bot_id> <channel_id> <title>
    """
    parts = message.text.split()
    if len(parts) < 4:
        await message.answer("Использование: /add_channel <bot_id> <channel_id> <title>")
        return

    bot_id = int(parts[1])
    channel_id = parts[2]
    title = " ".join(parts[3:])

    bot_instance = await bot_manager.get_bot(bot_id)
    if not await validate_channel(bot_instance, channel_id):
        await message.answer("Канал не найден или бот не имеет доступа.")
        return

    db.add_channel(bot_id=bot_id, title=title, channel_id=channel_id)
    await message.answer(f"Канал {title} успешно добавлен.")

def register_channel_handlers(dp: Dispatcher, db: Database, bot_manager):
    dp.register_message_handler(lambda m: add_channel_handler(m, db, bot_manager), commands=["add_channel"])
