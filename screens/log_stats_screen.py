from kivy.uix.screenmanager import Screen
from kivy.app import App

class LogStatsScreen(Screen):
    def back_to_control_panel(self):
        App.get_running_app().root.current = "control_panel"