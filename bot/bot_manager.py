from aiogram import Bot
from aiogram.exceptions import TelegramUnauthorizedError
import json
import os
import asyncio


class BotManager:
    def __init__(self, storage_path="data/bots.json"):
        self.storage_path = storage_path
        self.bots = {}
        self.active_token = None
        self._load_bots()

    def _load_bots(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding='utf-8') as f:
                    tokens = json.load(f)
                for token in tokens:
                    self.bots[token] = Bot(token=token)
                if tokens and not self.active_token:
                    self.active_token = tokens[0]
            except Exception as e:
                print(f"Ошибка загрузки ботов: {e}")

    def _save_bots(self):
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, "w", encoding='utf-8') as f:
                json.dump(list(self.bots.keys()), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения ботов: {e}")

    async def add_bot(self, token: str):
        token = token.strip()

        # Если бот уже есть, просто активируем его
        if token in self.bots:
            self.active_token = token
            self._save_bots()
            return self.bots[token]

        # Иначе добавляем нового бота
        bot = Bot(token=token)
        try:
            user = await bot.get_me()
            if not user:
                raise TelegramUnauthorizedError("Неверный токен")
        except TelegramUnauthorizedError:
            raise ValueError("Неверный токен Telegram")
        except Exception as e:
            raise ValueError(f"Ошибка подключения: {str(e)}")

        self.bots[token] = bot
        self.active_token = token
        self._save_bots()
        return bot

    def get_active_bot(self) -> Bot:
        if self.active_token and self.active_token in self.bots:
            return self.bots[self.active_token]
        return None

    def set_active_bot(self, token: str):
        if token in self.bots:
            self.active_token = token
            self._save_bots()
            return True
        return False

    def remove_bot(self, token):
        if token in self.bots:
            del self.bots[token]
            if self.active_token == token:
                self.active_token = list(self.bots.keys())[0] if self.bots else None
            self._save_bots()


# Глобальный экземпляр
bot_manager = BotManager()