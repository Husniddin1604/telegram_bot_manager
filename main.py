from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from screens.login_screen import LoginScreen
from screens.menu_screen import MenuScreen
from screens.send_screen import SendScreen

class MainScreenManager(SendScreen):
    pass

class MainApp(App):
    def build(self):
        sm = MainScreenManager()

        Builder.load_file("ui/login.kv")
        Builder.load_file("ui/menu.kv")
        Builder.load_file("ui/send.kv")

        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(SendScreen(name="send"))

        return sm

if __name__ == "__main__":
    MainApp().run()