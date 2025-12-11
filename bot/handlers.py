# bot/handlers.py
# Объединённый файл обработчиков для совместимости

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from db.database import Database

# Простое хранилище состояний
pending_channel_add = {}


def register_handlers(dp: Dispatcher, db: Database):
    """Регистрация всех обработчиков"""

    @dp.message(Command("start", "help"))
    async def start_handler(message: Message):
        """Обработчик /start и /help"""
        await message.answer(
            "Привет! Я Telegram Publisher Bot.\n\n"
            "Команды:\n"
            "/start - Начало работы\n"
            "/add_channel - Добавить канал\n"
            "/help - Эта справка"
        )

    @dp.message(Command("add_channel"))
    async def add_channel_command(message: Message):
        """Начало процесса добавления канала"""
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Добавить канал", callback_data="add_channel:start")],
            [InlineKeyboardButton(text="Помощь", callback_data="add_channel:help")],
        ])
        await message.answer(
            "Нажмите кнопку, чтобы начать добавление канала.",
            reply_markup=kb
        )

    @dp.callback_query(lambda c: c.data and c.data.startswith("add_channel:"))
    async def add_channel_callback(callback: CallbackQuery):
        """Обработка callback для добавления канала"""
        action = callback.data.split(":", 1)[1]
        user_id = callback.from_user.id

        if action == "start":
            await callback.message.answer(
                "Отправьте данные в формате:\n"
                "Название канала|@channel_or_id\n\n"
                "Пример: Мой канал|@my_news_channel"
            )
            pending_channel_add[user_id] = db
            await callback.answer("Введите данные в чате", show_alert=False)
        elif action == "help":
            await callback.answer(
                "Формат: Название|@channel_or_id. "
                "Канал должен быть доступен боту.",
                show_alert=True
            )

    @dp.message()
    async def text_handler(message: Message):
        """Обработка текстовых сообщений для добавления канала"""
        user_id = message.from_user.id

        if user_id not in pending_channel_add:
            return

        text = message.text.strip()
        parts = [p.strip() for p in text.split("|", 1)]

        if len(parts) != 2:
            await message.answer(
                "Неверный формат. Используйте:\n"
                "Название канала|@channel_or_id"
            )
            return

        title, channel_id = parts

        # Получаем первого бота из БД
        from db.models import Bot as BotModel
        session = db.SessionLocal()
        try:
            bot_obj = session.query(BotModel).first()
            if not bot_obj:
                await message.answer(
                    "В базе нет ни одного бота. "
                    "Добавьте бота через интерфейс приложения."
                )
                return

            # Добавляем канал
            db.add_channel(bot_id=bot_obj.id, title=title, channel_id=channel_id)
            await message.answer(
                f"✅ Канал <b>{title}</b> ({channel_id}) "
                f"добавлен к боту <b>{bot_obj.name}</b>."
            )
        except Exception as e:
            await message.answer(f"❌ Ошибка при добавлении канала: {e}")
        finally:
            session.close()
            pending_channel_add.pop(user_id, None)