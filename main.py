import os
print("Путь к изображению существует?", os.path.exists("assets/bot_icon.png"))
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.lang import Builder
from kivy.core.window import Window

from screens.menu_screen import MenuScreen
from screens.log_stats_screen import LogStatsScreen
from screens.login_screen import LoginScreen
from screens.create_publication_screen import CreatePublicationScreen

# Устанавливаем размер окна как у мобильного приложения
Window.size = (360, 640)


class MainScreenManager(ScreenManager):
    pass


class TelegramBotManager(App):
    def build(self):
        self.title = "Telegram Bot Manager"
        sm = MainScreenManager(transition=SlideTransition(direction='left'))

        # Загружаем kv файлы
        Builder.load_file("ui/menu.kv")
        Builder.load_file("ui/log_stats.kv")
        Builder.load_file("ui/login.kv")
        Builder.load_file("ui/create_publication.kv")

        # Добавляем экраны
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(LogStatsScreen(name="log_stats"))
        sm.add_widget(CreatePublicationScreen(name="create_publication"))

        return sm


if __name__ == "__main__":
    TelegramBotManager().run()