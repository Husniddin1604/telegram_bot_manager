from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from bot.bot_manager import bot_manager


class MenuScreen(Screen):
    def on_pre_enter(self):
        self.update_bot_info()

    def update_bot_info(self):
        """Обновляет информацию о текущем боте"""
        bot = bot_manager.get_active_bot()
        if bot:
            from bot.async_loop import async_loop
            future = async_loop.run(bot.get_me())

            def done(f):
                try:
                    bot_user = f.result()
                    # Сохраняем информацию о боте, но не показываем в этом меню
                    self.bot_info = f"@{bot_user.username}"
                except Exception:
                    self.bot_info = "Неизвестный бот"

            future.add_done_callback(done)
        else:
            self.bot_info = "Бот не подключен"

    def show_publications(self):
        self.show_development_message("Список публикаций")

    def create_publication(self):
        """Переход к созданию публикации"""
        if bot_manager.get_active_bot():
            App.get_running_app().root.current = "create_publication"
        else:
            self.show_error_message("Сначала подключите бота")

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

    def show_error_message(self, message):
        content = Label(text=message)
        popup = Popup(title='Ошибка',
                      content=content,
                      size_hint=(0.7, 0.3))
        popup.open()

    def back_to_previous(self):
        """Возврат к предыдущему экрану - на экран логина"""
        App.get_running_app().root.current = "login"