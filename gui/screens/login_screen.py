# gui/screens/login_screen.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import sqlalchemy.exc


class LoginScreen(Screen):
    token_input = ObjectProperty(None)
    bots_container = ObjectProperty(None)

    def on_pre_enter(self):
        """Заполняем список сохранёнными ботами."""
        self.refresh_bots_list()

    def refresh_bots_list(self):
        """Обновить список ботов"""
        app = App.get_running_app()
        session = app.db.SessionLocal()

        try:
            from db.models import Bot as BotModel
            bots = session.query(BotModel).all()
        finally:
            session.close()

        # Очистить контейнер
        self.bots_container.clear_widgets()

        if not bots:
            # Показать сообщение если ботов нет
            no_bots_label = Label(
                text="Нет сохранённых ботов",
                size_hint_y=None,
                height=40,
                color=(0.5, 0.5, 0.5, 1)
            )
            self.bots_container.add_widget(no_bots_label)
            return

        # Добавить кнопки для каждого бота
        for bot in bots:
            bot_box = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=50,
                spacing=10
            )

            # Кнопка выбора бота
            select_btn = Button(
                text=f"{bot.name} (ID: {bot.id})",
                size_hint_x=0.7
            )
            select_btn.bot_id = bot.id
            select_btn.bot_name = bot.name
            select_btn.bind(on_release=self.select_bot)

            # Кнопка удаления
            delete_btn = Button(
                text="Удалить",
                size_hint_x=0.3,
                background_color=(1, 0.3, 0.3, 1)
            )
            delete_btn.bot_id = bot.id
            delete_btn.bind(on_release=self.delete_bot)

            bot_box.add_widget(select_btn)
            bot_box.add_widget(delete_btn)
            self.bots_container.add_widget(bot_box)

    def add_bot(self):
        """Добавить нового бота"""
        token = self.token_input.text.strip()
        if not token:
            return

        app = App.get_running_app()

        try:
            # Генерируем имя бота
            bot_name = f"Bot_{token[:8]}"
            app.db.add_bot(name=bot_name, token=token)

            # Очистить поле ввода
            self.token_input.text = ""

            # Обновить список
            self.refresh_bots_list()

        except sqlalchemy.exc.IntegrityError:
            print("Бот с таким именем уже существует")
        except Exception as e:
            print(f"Ошибка при добавлении бота: {e}")

    def select_bot(self, button):
        """При выборе бота — переход в главное меню"""
        app = App.get_running_app()
        app.current_bot_id = button.bot_id
        app.current_bot_name = button.bot_name
        self.manager.current = "main_menu"

    def delete_bot(self, button):
        """Удалить бота"""
        app = App.get_running_app()
        session = app.db.SessionLocal()

        try:
            from db.models import Bot as BotModel
            bot = session.query(BotModel).filter(BotModel.id == button.bot_id).first()
            if bot:
                session.delete(bot)
                session.commit()
                self.refresh_bots_list()
        except Exception as e:
            print(f"Ошибка при удалении бота: {e}")
            session.rollback()
        finally:
            session.close()