from aiogram import Bot
from aiogram.exceptions import TelegramUnauthorizedError
import json
import os
import asyncio

class BotManager:
    def __init__(self, storage_path="data/bots.json"):
        self.storage_path= storage_path
        self.bots = {}
        self.active_token = None
        self._load_bots()

    def _load_bots(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                tokens=json.load(f)
            for token in tokens:
                self.bots[token] = Bot(token=token)
            if tokens:
                self.active_token = tokens[0]

    def _save_bots(self):
        with open(self.storage_path, "w") as f:
            json.dump(list(self.bots.keys()), f, indent=4)

    async def add_bot(self, token: str):
        bot = Bot(token=token)
        try:
            await bot.get_me()
        except TelegramUnauthorizedError:
            raise ValueError("Неверный токен Telegram")

        self.bots[token] = bot
        self.active_token = token
        self._save_bots()
        return bot

    def get_active_bot(self) -> Bot:
        if self.active_token:
            return self.bots.get(self.active_token)
        return None


    def set_active_bot(self, token: str):
        if token in self.bots:
            self.active_token = token
            return True
        return False

    def remove_bot(self, token):
        if token in self.bots:
            del self.bots[token]
            if self.active_token == token:
                self.active_token = list(self.bots.keys())[0] if self.bots else None

            self._save_bots()

bot_manager = BotManager()