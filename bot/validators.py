# bot/validators.py
# Валидация токенов и каналов

from aiogram import Bot as AiogramBot

async def validate_token(token: str) -> bool:
    try:
        bot = AiogramBot(token=token)
        me = await bot.get_me()
        await bot.session.close()
        return True if me else False
    except:
        return False

async def validate_channel(bot_instance, channel_id: str) -> bool:
    try:
        await bot_instance.get_chat(channel_id)
        return True
    except:
        return False
