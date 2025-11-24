from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock
import webbrowser
from bot.bot_manager import bot_manager
from bot.async_loop import async_loop


class LoginScreen(Screen):
    def on_enter(self):
        """При входе на экран обновляем список ботов"""
        self.update_bots_dropdown()
        self.ids.status.text = ""
        self.ids.token_input.text = ""
        self.ids.login_btn.disabled = False
        self.ids.login_btn.text = "Проверить токен"

    def update_bots_dropdown(self):
        """Обновляет список доступных ботов"""
        if bot_manager.bots:
            # Показываем выпадающий список
            self.ids.bots_spinner.values = list(bot_manager.bots.keys())
            self.ids.bots_spinner.text = "Выберите бота из списка"
            self.ids.bots_spinner.disabled = False
            self.ids.use_existing_btn.disabled = False
        else:
            # Скрываем выпадающий список, если ботов нет
            self.ids.bots_spinner.values = []
            self.ids.bots_spinner.text = "Нет сохраненных ботов"
            self.ids.bots_spinner.disabled = True
            self.ids.use_existing_btn.disabled = True

    def authenticate(self, token):
        token = token.strip()
        if not token:
            self.show_error("Введите API-токен")
            return

        # Проверяем, есть ли уже такой бот
        if token in bot_manager.bots:
            self.use_existing_bot(token)
            return

        self.ids.status.text = "[color=#FFA500]Проверка токена...[/color]"
        self.ids.login_btn.disabled = True
        self.ids.login_btn.text = "Проверка..."

        future = async_loop.run(bot_manager.add_bot(token))

        def done(f):
            self.ids.login_btn.disabled = False
            self.ids.login_btn.text = "Проверить токен"
            try:
                bot = f.result()
                # Получаем информацию о боте для отображения
                bot_info_future = async_loop.run(bot.get_me())

                def bot_info_done(f_info):
                    try:
                        bot_user = f_info.result()
                        self.show_success(f"Бот @{bot_user.username} успешно подключен!")
                        # Обновляем список ботов
                        self.update_bots_dropdown()
                        # Автоматически переходим в меню через 1.5 секунды
                        Clock.schedule_once(self.go_to_menu, 1.5)
                    except Exception as e:
                        self.show_error(f"Ошибка получения информации: {str(e)}")

                if bot_info_future:
                    bot_info_future.add_done_callback(bot_info_done)

            except Exception as e:
                self.show_error(f"Неверный токен: {str(e)}")

        if future:
            future.add_done_callback(done)

    def use_existing_bot(self, token=None):
        """Использует существующего бота из списка"""
        if not token:
            token = self.ids.bots_spinner.text

        if token in bot_manager.bots:
            bot_manager.set_active_bot(token)
            self.show_success("Бот выбран!")
            Clock.schedule_once(self.go_to_menu, 1.0)
        else:
            self.show_error("Выберите бота из списка")

    def go_to_menu(self, dt):
        """Переход в меню (вызывается через Clock)"""
        App.get_running_app().root.current = "menu"

    def show_error(self, message):
        self.ids.status.text = f"[color=#FF3333]{message}[/color]"

    def show_success(self, message):
        self.ids.status.text = f"[color=#33AA33]{message}[/color]"

    def open_botfather(self):
        """Открывает BotFather в Telegram"""
        webbrowser.open('https://t.me/BotFather')