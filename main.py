# main.py
import asyncio
import os
import threading

from gui.app import TelegramPublisherApp
from bot.dispatcher import start_bot_polling
from config import Config


async def run_bot():
    """Запуск бота без параметров"""
    await start_bot_polling()


def bot_thread_target():
    """Функция для запуска бота в отдельном потоке"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_bot())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем")
    finally:
        loop.close()


if __name__ == "__main__":
    # Создаём папку для БД и медиа
    os.makedirs("data", exist_ok=True)

    # Запускаем aiogram-бота в отдельном потоке
    if Config.APP_BOT_TOKEN:
        bot_thread = threading.Thread(target=bot_thread_target, daemon=True)
        bot_thread.start()
        print("Telegram бот запущен в фоновом потоке")
    else:
        print("APP_BOT_TOKEN не установлен - бот не запущен")

    # Запускаем Kivy GUI в главном потоке
    TelegramPublisherApp().run()