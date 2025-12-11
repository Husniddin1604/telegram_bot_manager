# bot/publisher.py
import os
from aiogram import Bot
from aiogram.types import InputFile

async def send_publication(db, pub, bot: Bot):
    try:
        if pub.media_path and os.path.exists(pub.media_path):
            await bot.send_photo(
                chat_id=pub.channel.channel_id,
                photo=InputFile(pub.media_path),
                caption=pub.text or ""
            )
        else:
            await bot.send_message(
                chat_id=pub.channel.channel_id,
                text=pub.text or "Пустой пост"
            )
        db.mark_sent(pub.id)
    except Exception as e:
        db.mark_error(pub.id, str(e))
        print(f"Ошибка отправки публикации {pub.id}: {e}")