# gui/app.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder

from db.database import Database
from gui.screens.login_screen import LoginScreen
from gui.screens.main_menu_screen import MainMenuScreen
from gui.screens.publish_screen import PublishScreen
from gui.screens.publications_list_screen import PublicationsListScreen
from gui.screens.settings_screen import SettingsScreen

from gui.themes.light_theme import LightTheme


class RootManager(ScreenManager):
    pass


class TelegramPublisherApp(App):
    db: Database = None
    theme: dict = None
    current_bot_id: int = None
    current_bot_name: str = None

    def build(self):
        self.title = "Telegram Publisher"
        Window.size = (420, 720)

        # Загружаем темы по умолчанию (light)
        self.theme = LightTheme().colors

        # Инициируем БД
        from config import Config
        self.db = Database(encryption_key=Config.ENCRYPT_KEY)
        self.db.init_db()

        # Загружаем KV файлы
        try:
            Builder.load_file("gui/kv/login.kv")
            Builder.load_file("gui/kv/main_menu.kv")
            Builder.load_file("gui/kv/publish.kv")
            Builder.load_file("gui/kv/publications_list.kv")
            Builder.load_file("gui/kv/settings.kv")
        except Exception as e:
            print(f"Ошибка загрузки KV файлов: {e}")
            raise

        sm = RootManager(transition=FadeTransition())
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MainMenuScreen(name="main_menu"))
        sm.add_widget(PublishScreen(name="publish"))
        sm.add_widget(PublicationsListScreen(name="publications_list"))
        sm.add_widget(SettingsScreen(name="settings"))

        # Обновление публикаций каждые 5 сек
        Clock.schedule_interval(self.update_publications, 5)

        return sm

    def update_publications(self, dt):
        """Обновить список публикаций"""
        try:
            if hasattr(self.root, 'get_screen'):
                screen = self.root.get_screen("publications_list")
                if self.root.current == "publications_list":
                    screen.refresh()
        except Exception as e:
            pass  # Игнорируем ошибки


if __name__ == "__main__":
    TelegramPublisherApp().run()