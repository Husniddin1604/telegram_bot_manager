# gui/screens/main_menu_screen.py
from kivy.uix.screenmanager import Screen

class MainMenuScreen(Screen):
    def go_publish(self):
        self.manager.current = "publish"

    def go_publications(self):
        self.manager.current = "publications_list"

    def go_settings(self):
        self.manager.current = "settings"
