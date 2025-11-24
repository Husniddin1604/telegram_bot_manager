from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from bot.sender import send_message
from bot.async_loop import async_loop
from bot.bot_manager import bot_manager


class SendScreen(Screen):
    def on_pre_enter(self):
        """Вызывается перед показом экрана"""
        self.update_bot_info()

    def update_bot_info(self):
        """Обновляет информацию о текущем боте"""
        bot = bot_manager.get_active_bot()
        if bot:
            from bot.async_loop import async_loop
            future = async_loop.run(bot.get_me())

            def done(f):
                try:
                    bot_user = f.result()
                    self.ids.bot_info.text = f"Отправка через: @{bot_user.username}"
                    self.ids.bot_info.color = (0.2, 0.2, 0.2, 1)
                except Exception:
                    self.ids.bot_info.text = "Отправка через: Неизвестный бот"
                    self.ids.bot_info.color = (0.8, 0.2, 0.2, 1)

            if future:
                future.add_done_callback(done)
        else:
            self.ids.bot_info.text = "Бот не выбран"
            self.ids.bot_info.color = (0.8, 0.2, 0.2, 1)

    def send_message(self):
        """Основная функция отправки сообщения"""
        chat_id = self.ids.chat_id_input.text.strip()
        message_text = self.ids.message_input.text.strip()

        # Проверяем активного бота
        bot = bot_manager.get_active_bot()
        if not bot:
            self.show_status("Сначала выберите бота", error=True)
            return

        # Проверяем ввод данных
        if not chat_id:
            self.show_status("Введите chat_id канала/группы", error=True)
            return

        if not message_text:
            self.show_status("Введите текст сообщения", error=True)
            return

        # Блокируем кнопку во время отправки
        self.ids.send_btn.disabled = True
        self.ids.send_btn.text = "Отправка..."
        self.show_status("Отправка сообщения...", warning=True)

        # Отправляем сообщение через асинхронный цикл
        future = async_loop.run(send_message(bot, chat_id, message_text))

        def done(f):
            # Разблокируем кнопку
            self.ids.send_btn.disabled = False
            self.ids.send_btn.text = "Отправить сообщение"

            try:
                result = f.result()
                if result is True:
                    self.show_status("Сообщение успешно отправлено!", success=True)
                    # Очищаем поле сообщения после успешной отправки
                    self.ids.message_input.text = ""
                else:
                    self.show_status(result, error=True)
            except Exception as e:
                self.show_status(f"Ошибка: {str(e)}", error=True)

        if future:
            future.add_done_callback(done)

    def show_status(self, message, error=False, warning=False, success=False):
        """Показывает статусное сообщение"""
        if error:
            self.ids.status.text = f"[color=ff3333]{message}[/color]"
        elif warning:
            self.ids.status.text = f"[color=ffaa00]{message}[/color]"
        elif success:
            self.ids.status.text = f"[color=33aa33]{message}[/color]"
        else:
            self.ids.status.text = message

    def show_help(self):
        """Показывает справку по получению chat_id"""
        help_text = """
Как получить chat_id:

1. Для каналов:
   - Добавьте бота в канал как администратора
   - Отправьте любое сообщение в канал
   - Используйте @chatidrobot бота чтобы узнать ID

2. Для групп:
   - Добавьте бота в группу
   - Отправьте сообщение в группе
   - Бот получит ID автоматически

3. Формат chat_id:
   - Каналы: -100xxxxxxxxxx
   - Группы: -xxxxxxxxxx
   - Пользователи: xxxxxxxxx

Примеры:
   - Канал: -1001234567890
   - Группа: -123456789
   - Пользователь: 123456789
"""
        content = Label(text=help_text, text_size=(400, None))
        popup = Popup(title='Справка: Как получить chat_id',
                      content=content,
                      size_hint=(0.9, 0.8))
        popup.open()

    def back_to_menu(self):
        """Возврат в главное меню"""
        App.get_running_app().root.current = "menu"