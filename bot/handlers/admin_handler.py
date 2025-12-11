# bot/handlers/admin_handler.py
# Обработчики админ-команд

from aiogram import types
from aiogram.dispatcher import Dispatcher

async def start_handler(message: types.Message):
    await message.answer("Привет! Я Telegram Publisher Bot. Используй /add_channel для добавления канала.")

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
