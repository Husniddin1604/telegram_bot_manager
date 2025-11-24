from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import re
from bot.sender import send_message, extract_new_chat_id_from_error
from bot.async_loop import async_loop
from bot.bot_manager import bot_manager
from bot.chat_manager import chat_manager


class CreatePublicationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.schedule_date = None
        self.schedule_time = None
        self.repeat_mode = "Не повторять"
        self.media_path = None

    def on_pre_enter(self):
        """При входе на экран"""
        self.update_channels_list()

    def update_channels_list(self):
        """Обновляет список каналов/групп"""
        chats = chat_manager.get_chats()
        if chats:
            chat_names = []
            for chat in chats:
                chat_type_symbol = ""
                if chat['type'] == 'channel':
                    chat_type_symbol = "📢 "
                elif chat['type'] == 'supergroup':
                    chat_type_symbol = "👥 "
                elif chat['type'] == 'group':
                    chat_type_symbol = "👤 "
                elif chat['type'] == 'private':
                    chat_type_symbol = "🔒 "

                chat_names.append(f"{chat_type_symbol}{chat['name']} ({chat['chat_id']})")

            self.ids.channel_spinner.values = chat_names
            if chat_names:
                self.ids.channel_spinner.text = chat_names[0]
        else:
            self.ids.channel_spinner.values = ["Нет сохраненных чатов"]
            self.ids.channel_spinner.text = "Нет сохраненных чатов"

    def discover_chats(self):
        """Обнаруживает чаты автоматически"""
        bot = bot_manager.get_active_bot()
        if not bot:
            self.show_status("Сначала выберите бота", error=True)
            return

        self.show_status("Поиск чатов...", warning=True)

        future = async_loop.run(chat_manager.discover_chats(bot))

        def done(f):
            try:
                discovered_chats = f.result()
                for chat in discovered_chats:
                    chat_manager.add_chat(chat["chat_id"], chat["name"], chat["type"])

                self.update_channels_list()
                if discovered_chats:
                    self.show_status(f"Найдено {len(discovered_chats)} чатов", success=True)
                else:
                    self.show_status("Чаты не найдены. Убедитесь, что бот добавлен в чаты и есть сообщения", error=True)
            except Exception as e:
                self.show_status(f"Ошибка поиска: {str(e)}", error=True)

        if future:
            future.add_done_callback(done)

    def add_chat_manually(self):
        """Добавляет чат вручную"""
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        chat_id_input = TextInput(
            hint_text='Введите chat_id (например: -1001234567890)',
            multiline=False,
            size_hint_y=None,
            height=40
        )

        chat_name_input = TextInput(
            hint_text='Введите название чата',
            multiline=False,
            size_hint_y=None,
            height=40
        )

        layout.add_widget(Label(text='Добавить чат вручную:'))
        layout.add_widget(Label(text='Chat ID:'))
        layout.add_widget(chat_id_input)
        layout.add_widget(Label(text='Название:'))
        layout.add_widget(chat_name_input)

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)

        def add_chat(dt):
            chat_id = chat_id_input.text.strip()
            name = chat_name_input.text.strip()

            if chat_id and name:
                # Проверяем валидность chat_id
                try:
                    int(chat_id)
                    if chat_manager.add_chat(chat_id, name):
                        self.update_channels_list()
                        self.show_status("Чат добавлен", success=True)
                        popup.dismiss()
                    else:
                        self.show_status("Чат уже существует", error=True)
                except ValueError:
                    self.show_status("Chat ID должен быть числом", error=True)
            else:
                self.show_status("Заполните все поля", error=True)

        add_btn = Button(text='Добавить', background_color=(0.2, 0.6, 0.8, 1))
        add_btn.bind(on_release=add_chat)

        cancel_btn = Button(text='Отмена', background_color=(0.8, 0.3, 0.3, 1))
        cancel_btn.bind(on_release=lambda x: popup.dismiss())

        btn_layout.add_widget(add_btn)
        btn_layout.add_widget(cancel_btn)
        layout.add_widget(btn_layout)

        popup = Popup(title='Добавить чат', content=layout, size_hint=(0.8, 0.5))
        popup.open()

    def handle_migration_error(self, error_message, old_chat_id):
        """Обрабатывает ошибку миграции чата"""
        new_chat_id = extract_new_chat_id_from_error(error_message)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        if new_chat_id:
            message = f"Группа была преобразована в супергруппу.\nНовый chat_id: {new_chat_id}\n\nХотите автоматически обновить chat_id?"

            def update_chat(dt):
                if chat_manager.update_chat_id(old_chat_id, new_chat_id):
                    self.update_channels_list()
                    self.show_status("Chat_ID обновлен автоматически", success=True)
                popup.dismiss()

            update_btn = Button(text='Обновить автоматически', background_color=(0.2, 0.6, 0.8, 1))
            update_btn.bind(on_release=update_chat)
            layout.add_widget(update_btn)
        else:
            message = "Группа была преобразована в супергруппу. Получите новый chat_id и добавьте его вручную."

        layout.add_widget(Label(text=message))

        manual_btn = Button(text='Добавить вручную', background_color=(0.8, 0.5, 0.2, 1))
        manual_btn.bind(on_release=lambda x: (popup.dismiss(), self.add_chat_manually()))
        layout.add_widget(manual_btn)

        close_btn = Button(text='Закрыть', background_color=(0.8, 0.3, 0.3, 1))
        close_btn.bind(on_release=lambda x: popup.dismiss())
        layout.add_widget(close_btn)

        popup = Popup(title='Ошибка миграции чата', content=layout, size_hint=(0.8, 0.5))
        popup.open()

    def send_publication(self):
        """Отправка публикации"""
        # Проверяем активного бота
        bot = bot_manager.get_active_bot()
        if not bot:
            self.show_status("Сначала выберите бота в главном меню", error=True)
            return

        # Проверяем выбор канала
        selected_chat = self.ids.channel_spinner.text
        if selected_chat == "Нет сохраненных чатов":
            self.show_status("Сначала добавьте чат", error=True)
            return

        # Извлекаем chat_id из выбранного элемента
        try:
            chat_id = re.search(r'\((-?\d+)\)', selected_chat).group(1)
        except:
            self.show_status("Ошибка получения chat_id", error=True)
            return

        # Проверяем текст публикации
        text = self.ids.publication_text.text.strip()
        if not text:
            self.show_status("Введите текст публикации", error=True)
            return

        self.send_to_telegram(chat_id, text)

    def send_to_telegram(self, chat_id, text):
        """Отправляет сообщение в Telegram"""
        bot = bot_manager.get_active_bot()

        self.ids.send_btn.disabled = True
        self.ids.send_btn.text = "Отправка..."
        self.show_status("Отправка публикации...", warning=True)

        future = async_loop.run(send_message(bot, chat_id, text))

        def done(f):
            self.ids.send_btn.disabled = False
            self.ids.send_btn.text = "Отправить"

            try:
                result = f.result()
                if result is True:
                    self.show_status("Публикация успешно отправлена!", success=True)
                    # Очищаем поле текста после успешной отправки
                    self.ids.publication_text.text = ""
                else:
                    # Проверяем, является ли ошибка ошибкой миграции
                    if "преобразована в супергруппу" in result:
                        self.handle_migration_error(result, chat_id)
                    else:
                        self.show_status(result, error=True)
            except Exception as e:
                self.show_status(f"Ошибка: {str(e)}", error=True)

        if future:
            future.add_done_callback(done)

    def show_status(self, message, error=False, warning=False, success=False):
        """Показывает статусное сообщение - ДОБАВЛЕННЫЙ МЕТОД"""
        if error:
            self.ids.status_label.text = f"[color=ff3333]{message}[/color]"
        elif warning:
            self.ids.status_label.text = f"[color=ffaa00]{message}[/color]"
        elif success:
            self.ids.status_label.text = f"[color=33aa33]{message}[/color]"
        else:
            self.ids.status_label.text = message

    def add_button(self):
        """Добавление инлайн-кнопки (заглушка)"""
        self.show_development_message("Добавление инлайн-кнопок")

    def add_media(self):
        """Добавление медиа (заглушка)"""
        self.show_development_message("Добавление медиа")

    def show_schedule_popup(self):
        """Показывает попап для выбора даты и времени"""
        content = Label(text="Функционал планирования в разработке")
        popup = Popup(title='Выбор даты и времени',
                      content=content,
                      size_hint=(0.8, 0.4))
        popup.open()

    def show_repeat_popup(self):
        """Показывает попап для выбора повторения"""
        content = Label(text="Функционал повторения в разработке")
        popup = Popup(title='Настройка повторения',
                      content=content,
                      size_hint=(0.8, 0.4))
        popup.open()

    def save_as_template(self):
        """Сохранение как шаблона (заглушка)"""
        self.show_development_message("Сохранение как шаблона")

    def show_development_message(self, feature_name):
        """Показывает сообщение о разработке"""
        content = Label(text=f"Функционал '{feature_name}' в разработке")
        popup = Popup(title='В разработке',
                      content=content,
                      size_hint=(0.7, 0.3))
        popup.open()

    def back_to_menu(self):
        """Возврат в главное меню"""
        App.get_running_app().root.current = "menu"