import json
import os
import re
from aiogram import Bot


class ChatManager:
    def __init__(self, storage_path="data/chats.json"):
        self.storage_path = storage_path
        self.chats = []
        self._load_chats()

    def _load_chats(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding='utf-8') as f:
                    self.chats = json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки чатов: {e}")
                self.chats = []

    def _save_chats(self):
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, "w", encoding='utf-8') as f:
                json.dump(self.chats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения чатов: {e}")

    def add_chat(self, chat_id, name, chat_type="unknown"):
        """Добавляет чат в список"""
        chat_info = {
            "chat_id": chat_id,
            "name": name,
            "type": chat_type
        }

        # Проверяем, нет ли уже такого chat_id
        for chat in self.chats:
            if chat["chat_id"] == chat_id:
                return False

        self.chats.append(chat_info)
        self._save_chats()
        return True

    def update_chat_id(self, old_chat_id, new_chat_id):
        """Обновляет chat_id для мигрировавшего чата"""
        for chat in self.chats:
            if chat["chat_id"] == old_chat_id:
                chat["chat_id"] = new_chat_id
                self._save_chats()
                return True
        return False

    def get_chats(self):
        return self.chats

    def remove_chat(self, chat_id):
        self.chats = [chat for chat in self.chats if chat["chat_id"] != chat_id]
        self._save_chats()

    async def discover_chats(self, bot: Bot):
        """Автоматически обнаруживает чаты, в которых есть бот"""
        try:
            updates = await bot.get_updates(limit=100)
            discovered_chats = []

            for update in updates:
                if update.message:
                    chat = update.message.chat
                    chat_type = self._get_chat_type(chat)

                    chat_name = (
                        chat.title if chat.title else
                        chat.username if chat.username else
                        f"{chat.first_name} {chat.last_name}" if chat.first_name else
                        str(chat.id)
                    )

                    discovered_chats.append({
                        "chat_id": str(chat.id),
                        "name": chat_name,
                        "type": chat_type
                    })

            return discovered_chats
        except Exception as e:
            print(f"Ошибка обнаружения чатов: {e}")
            return []

    def _get_chat_type(self, chat):
        """Определяет тип чата"""
        if hasattr(chat, 'type'):
            if chat.type == "private":
                return "private"
            elif chat.type == "group":
                return "group"
            elif chat.type == "supergroup":
                return "supergroup"
            elif chat.type == "channel":
                return "channel"
        return "unknown"


# Глобальный экземпляр
chat_manager = ChatManager()