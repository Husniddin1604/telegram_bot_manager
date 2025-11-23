from kivy.uix.screenmanager import Screen
from bot.sender import send_message
from bot.async_loop import async_loop
from bot.bot_manager import bot_manager

class SendScreen(Screen):
    def send(self, chat_id, text):
        bot = bot_manager.get_active_bot()
        if not bot:
            self.ids.status.text = "[color=ff3333]Нет активного бота[/color]"
            return

        if not chat_id.strip() or not text.strip():
            self.ids.status.text = "[color=ff3333]Заполните все поля[/color]"
            return

        future = async_loop.run(send_message(bot, chat_id, text))

        def done(f):
            result = f.result()
            if result is True:
                self.ids.status.text = "[color=33ff33]Отправлено[/color]"
            else:
                self.ids.status.text = f"[color=ff33ff]{result}[/color]"

        future.add_done_callback(done)

    def back(self):
        self.manager.current = "menu"