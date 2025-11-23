from kivy.uix.screenmanager import Screen
from kivy.app import App
from bot.bot_manager import bot_manager


class MenuScreen(Screen):
    def on_pre_enter(self):
        self.update_bot_info()

    def update_bot_info(self):
        bot = bot_manager.get_active_bot()
        if bot:
            from bot.async_loop import async_loop
            future = async_loop.run(bot.get_me())

            def done(f):
                try:
                    bot_user = f.result()
                    self.ids.bot_label.text = f"Подключен: @{bot_user.username}"
                    self.ids.bot_info.text = f"{bot_user.first_name}\nID: {bot_user.id}"
                except Exception:
                    self.ids.bot_label.text = "Подключен: Неизвестный бот"
                    self.ids.bot_info.text = "Не удалось загрузить информацию"

            future.add_done_callback(done)
        else:
            self.ids.bot_label.text = "Бот не подключен"
            self.ids.bot_info.text = "Нажмите 'Подключить бота' для начала работы"

    def go_send(self):
        if bot_manager.get_active_bot():
            App.get_running_app().root.current = "send"
        else:
            self.ids.bot_info.text = "[color=#FF3333]Сначала подключите бота[/color]"

    def go_control_panel(self):
        """Переход к панели управления"""
        App.get_running_app().root.current = "control_panel"

    def go_bots(self):
        App.get_running_app().root.current = "bots"

    def go_login(self):
        App.get_running_app().root.current = "login"