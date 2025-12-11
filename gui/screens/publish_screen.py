# gui/screens/publish_screen.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from datetime import datetime


class PublishScreen(Screen):
    channel_spinner = ObjectProperty(None)
    text_input = ObjectProperty(None)
    date_input = ObjectProperty(None)
    time_input = ObjectProperty(None)
    media_path_label = ObjectProperty(None)

    selected_media_path = StringProperty("")

    def on_pre_enter(self):
        """Загрузить список каналов при входе на экран"""
        self.load_channels()

        # Установить текущую дату и время
        now = datetime.now()
        self.date_input.text = now.strftime("%Y-%m-%d")
        self.time_input.text = now.strftime("%H:%M")

    def load_channels(self):
        """Загрузить список каналов в Spinner"""
        app = App.get_running_app()
        session = app.db.SessionLocal()

        try:
            from db.models import Channel

            # Получить каналы текущего бота
            if app.current_bot_id:
                channels = session.query(Channel).filter(
                    Channel.bot_id == app.current_bot_id
                ).all()
            else:
                channels = session.query(Channel).all()

            if channels:
                self.channel_spinner.values = [
                    f"{c.title} ({c.channel_id})" for c in channels
                ]
                self._channel_map = {
                    f"{c.title} ({c.channel_id})": c.id for c in channels
                }
                self.channel_spinner.text = self.channel_spinner.values[0]
            else:
                self.channel_spinner.values = ["Нет каналов"]
                self.channel_spinner.text = "Нет каналов"
                self._channel_map = {}

        except Exception as e:
            print(f"Ошибка загрузки каналов: {e}")
            self.channel_spinner.values = ["Ошибка загрузки"]
            self._channel_map = {}
        finally:
            session.close()

    def choose_media(self):
        """Открыть диалог выбора файла"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        filechooser = FileChooserListView(
            filters=['*.jpg', '*.jpeg', '*.png', '*.gif', '*.mp4', '*.avi']
        )

        buttons = BoxLayout(size_hint_y=None, height=50, spacing=10)

        popup = Popup(
            title="Выберите медиа файл",
            content=content,
            size_hint=(0.9, 0.9)
        )

        def select_file(instance):
            if filechooser.selection:
                self.selected_media_path = filechooser.selection[0]
                self.media_path_label.text = filechooser.selection[0].split('/')[-1]
            popup.dismiss()

        select_btn = Button(text="Выбрать")
        select_btn.bind(on_release=select_file)

        cancel_btn = Button(text="Отмена")
        cancel_btn.bind(on_release=popup.dismiss)

        buttons.add_widget(cancel_btn)
        buttons.add_widget(select_btn)

        content.add_widget(filechooser)
        content.add_widget(buttons)

        popup.open()

    def save_publication(self):
        """Сохранить публикацию"""
        app = App.get_running_app()

        # Проверка на наличие текущего бота
        if not app.current_bot_id:
            self.show_error("Выберите бота на экране входа")
            return

        # Получить ID выбранного канала
        selected_channel_text = self.channel_spinner.text
        if selected_channel_text not in self._channel_map:
            self.show_error("Выберите канал")
            return

        channel_db_id = self._channel_map[selected_channel_text]
        text = self.text_input.text.strip()
        media = self.selected_media_path if self.selected_media_path else None

        # Проверка: должен быть текст или медиа
        if not text and not media:
            self.show_error("Введите текст или выберите медиа")
            return

        # Парсинг даты и времени
        try:
            date_str = self.date_input.text.strip()
            time_str = self.time_input.text.strip()
            dt = datetime.fromisoformat(f"{date_str} {time_str}")

            # Проверка: дата должна быть в будущем
            if dt < datetime.now():
                self.show_error("Дата и время должны быть в будущем")
                return

        except ValueError:
            self.show_error("Неверный формат даты/времени")
            return

        # Сохранить публикацию
        try:
            app.db.add_publication(
                bot_id=app.current_bot_id,
                channel_db_id=channel_db_id,
                text=text,
                media_path=media,
                scheduled_time=dt,
            )

            # Очистить форму
            self.text_input.text = ""
            self.selected_media_path = ""
            self.media_path_label.text = "Не выбран"

            # Показать успех
            self.show_success("Публикация сохранена!")

            # Перейти к списку публикаций
            self.manager.current = "publications_list"

        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            self.show_error(f"Ошибка: {str(e)}")

    def inline_buttons_popup(self):
        """Показать popup о функции в разработке"""
        Popup(
            title="Inline кнопки",
            content=Label(text="Функция находится в разработке"),
            size_hint=(0.6, 0.3)
        ).open()

    def show_error(self, message):
        """Показать сообщение об ошибке"""
        Popup(
            title="Ошибка",
            content=Label(text=message),
            size_hint=(0.7, 0.3)
        ).open()

    def show_success(self, message):
        """Показать сообщение об успехе"""
        popup = Popup(
            title="Успех",
            content=Label(text=message),
            size_hint=(0.6, 0.3)
        )
        popup.open()
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)