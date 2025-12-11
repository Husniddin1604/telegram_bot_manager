# gui/screens/settings_screen.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App


class SettingsScreen(Screen):
    bot_name_input = ObjectProperty(None)
    theme_toggle = ObjectProperty(None)

    def toggle_theme(self):
        app = App.get_running_app()
        if self.theme_toggle.state == "down":
            from gui.themes.dark_theme import DarkTheme
            app.theme = DarkTheme().colors
        else:
            from gui.themes.light_theme import LightTheme
            app.theme = LightTheme().colors

    def add_channel(self):
        """Открывает инструкцию — использовать /add_channel в Telegram."""
        import webbrowser
        webbrowser.open("https://t.me/your_bot?start=add_channel")
