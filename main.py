from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.lang import Builder
from kivy.core.window import Window

from screens.login_screen import LoginScreen
from screens.menu_screen import MenuScreen
from screens.send_screen import SendScreen
from screens.bots_screen import BotsScreen
from screens.control_panel_screen import ControlPanelScreen
from screens.log_stats_screen import LogStatsScreen

# Устанавливаем размер окна
Window.size = (400, 600)


class MainScreenManager(ScreenManager):
    pass


class TelegramBotManager(App):
    def build(self):
        self.title = "Telegram Bot Manager"
        sm = MainScreenManager(transition=SlideTransition(direction='left'))

        # Загружаем все kv файлы
        Builder.load_file("ui/login.kv")
        Builder.load_file("ui/menu.kv")
        Builder.load_file("ui/send.kv")
        Builder.load_file("ui/bots.kv")
        Builder.load_file("ui/control_panel.kv")
        Builder.load_file("ui/log_stats.kv")

        # Добавляем все экраны
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(SendScreen(name="send"))
        sm.add_widget(BotsScreen(name="bots"))
        sm.add_widget(ControlPanelScreen(name="control_panel"))
        sm.add_widget(LogStatsScreen(name="log_stats"))

        return sm


if __name__ == "__main__":
    TelegramBotManager().run()