from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class ControlPanelScreen(Screen):
    def show_publications(self):
        self.show_development_message("Список публикаций")

    def create_publication(self):
        self.show_development_message("Создание публикации")

    def show_templates(self):
        self.show_development_message("Шаблоны")

    def show_settings(self):
        self.show_development_message("Настройки")

    def show_log_stats(self):
        App.get_running_app().root.current = "log_stats"

    def show_development_message(self, feature_name):
        content = Label(text=f"Функционал '{feature_name}' в разработке")
        popup = Popup(title='В разработке',
                      content=content,
                      size_hint=(0.7, 0.3))
        popup.open()

    def back_to_menu(self):
        App.get_running_app().root.current = "menu"