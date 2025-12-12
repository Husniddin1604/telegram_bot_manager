from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError, TelegramNetworkError
import asyncio
import re


async def send_message(bot: Bot, chat_id: str, text: str):
    try:
        # Убираем возможные пробелы
        chat_id = chat_id.strip()
        text = text.strip()

        # Проверяем формат chat_id
        if not is_valid_chat_id(chat_id):
            return "Ошибка: Неверный формат chat_id. Должен быть числом (например: 123456789 или -1001234567890)"

        # Пытаемся отправить сообщение
        await bot.send_message(chat_id=chat_id, text=text)
        return True

    except TelegramBadRequest as e:
        error_message = str(e).lower()

        if "chat not found" in error_message:
            return "Ошибка: Чат не найден. Проверьте chat_id и убедитесь, что бот добавлен в чат"
        elif "bot was blocked" in error_message:
            return "Ошибка: Бот заблокирован в этом чате"
        elif "not enough rights" in error_message:
            return "Ошибка: Недостаточно прав для отправки сообщений"
        elif "group chat was upgraded" in error_message or "migrated" in error_message:
            # Извлекаем новый chat_id из ошибки
            new_chat_id = extract_new_chat_id_from_error(str(e))
            if new_chat_id:
                return f"Ошибка: Группа преобразована в супергруппу. Используйте новый chat_id: {new_chat_id}"
            else:
                return "Ошибка: Группа преобразована в супергруппу. Получите новый chat_id"
        elif "chat not exist" in error_message:
            return "Ошибка: Чат не существует или бот не является его участником"
        else:
            return f"Ошибка запроса Telegram: {e}"

    except TelegramForbiddenError:
        return "Ошибка: Бот не может писать в этот чат/канал. Проверьте права бота"

    except TelegramNetworkError:
        return "Ошибка сети: Проверьте подключение к интернету"

    except Exception as e:
        return f"Неизвестная ошибка: {e}"


def is_valid_chat_id(chat_id):
    """Проверяет валидность chat_id"""
    try:
        # Chat_id должен быть числом (может быть отрицательным для групп/каналов)
        int(chat_id)
        return True
    except ValueError:
        return False


def extract_new_chat_id_from_error(error_message):
    patterns = [
        r'with id\s*:(-?\d+)',
        r'new chat id\s*:(-?\d+)',
        r'id\s*(-?\d+)',
        r'(-100\d+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, error_message)
        if match:
            return match.group(1)

    return None