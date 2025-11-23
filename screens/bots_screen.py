from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from bot.bot_manager import bot_manager


class BotsScreen(Screen):
    def on_pre_enter(self):
        """Вызывается перед показом экрана"""
        self.update_bots_list()

    def update_bots_list(self):
        """Обновляет список ботов"""
        # Очищаем список
        self.ids.bots_list.clear_widgets()

        # Если ботов нет, показываем сообщение
        if not bot_manager.bots:
            no_bots_label = Label(
                text="Нет добавленных ботов",
                size_hint_y=None,
                height=40,
                color=[0.5, 0.5, 0.5, 1]
            )
            self.ids.bots_list.add_widget(no_bots_label)
            return

        # Добавляем каждого бота в список
        for token in bot_manager.bots.keys():
            bot_item = self.create_bot_item(token)
            self.ids.bots_list.add_widget(bot_item)

    def create_bot_item(self, token):
        """Создает элемент списка для одного бота"""
        layout = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=10,
            padding=[10, 5]
        )

        # Обрезаем токен для отображения
        display_token = f"{token[:15]}...{token[-10:]}" if len(token) > 25 else token

        # Метка с токеном
        token_label = Label(
            text=display_token,
            text_size=(200, None),
            halign='left',
            valign='middle'
        )

        # Кнопка выбора бота
        select_btn = Button(
            text='Выбрать' if bot_manager.active_token != token else '✓ Активный',
            size_hint_x=0.4,
            background_color=[0.2, 0.6, 0.8, 1] if bot_manager.active_token != token else [0.2, 0.8, 0.3, 1]
        )
        select_btn.bind(on_release=lambda btn, t=token: self.select_bot(t))

        # Кнопка удаления бота
        remove_btn = Button(
            text='Удалить',
            size_hint_x=0.4,
            background_color=[0.8, 0.3, 0.3, 1]
        )
        remove_btn.bind(on_release=lambda btn, t=token: self.remove_bot(t))

        layout.add_widget(token_label)
        layout.add_widget(select_btn)
        layout.add_widget(remove_btn)

        return layout

    def select_bot(self, token):
        """Выбирает бота как активного"""
        if bot_manager.set_active_bot(token):
            self.update_bots_list()
            # Показываем сообщение об успехе
            self.ids.status.text = "[color=#33AA33]Бот выбран как активный[/color]"

    def remove_bot(self, token):
        """Удаляет бота"""
        bot_manager.remove_bot(token)
        self.update_bots_list()
        # Показываем сообщение
        self.ids.status.text = "[color=#FF3333]Бот удален[/color]"

    def back_to_menu(self):
        """Возвращает в главное меню"""
        App.get_running_app().root.current = "menu"