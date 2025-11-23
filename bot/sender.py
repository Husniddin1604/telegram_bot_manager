from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest


async def send_message(bot: Bot, chat_id:str, text: str):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        return True

    except TelegramBadRequest as e:
        return f"Ошибка: {e}"