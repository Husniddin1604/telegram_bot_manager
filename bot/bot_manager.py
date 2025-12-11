# bot/bot_manager.py (исправленная версия)
import asyncio
from aiogram import Bot as AiogramBot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from db.database import Database


class BotManager:
    """
    Кэширует экземпляры Aiogram-ботов по bot_id
    """

    def __init__(self, db: Database):
        self.db = db
        self.bots = {}  # bot_id -> AiogramBot

    async def get_bot(self, bot_id: int) -> AiogramBot:
        """Получить или создать экземпляр бота"""
        if bot_id in self.bots:
            return self.bots[bot_id]

        token = self.db.get_bot_token(bot_id)

        # Правильный способ для Aiogram 3.7.0+
        bot = AiogramBot(
            token=token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

        self.bots[bot_id] = bot
        return bot

    async def close_bot(self, bot_id: int):
        """Закрыть сессию бота"""
        if bot_id in self.bots:
            await self.bots[bot_id].session.close()
            del self.bots[bot_id]

    async def close_all(self):
        """Закрыть все сессии ботов"""
        for bot_id in list(self.bots.keys()):
            await self.close_bot(bot_id)