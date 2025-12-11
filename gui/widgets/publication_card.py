# gui/widgets/publication_card.py
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ColorProperty
from kivy.lang import Builder
from kivy.uix.button import Button

Builder.load_string("""
<PublicationCard>:
    orientation: "horizontal"
    size_hint_y: None
    height: "60dp"
    padding: "10dp"
    spacing: "10dp"
    canvas.before:
        Color:
            rgba: root.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10,]
    Label:
        text: root.channel_title
        size_hint_x: 0.4
        color: 0,0,0,1
        bold: True
    Label:
        text: root.status_text
        size_hint_x: 0.3
        color: root.status_color
    BoxLayout:
        size_hint_x: 0.3
        spacing: "5dp"
        Button:
            text: "✏️"
            on_release: root.on_edit(root.pub_id)
            background_color: 0.2, 0.6, 1, 1
        Button:
            text: "🗑️"
            on_release: root.on_delete(root.pub_id)
            background_color: 1, 0.2, 0.2, 1
""")

class PublicationCard(BoxLayout):
    pub_id = NumericProperty(0)
    channel_title = StringProperty("")
    status_text = StringProperty("")
    status_color = ColorProperty([0, 0, 1, 1])  # default blue
    on_edit = ObjectProperty(lambda x: None)
    on_delete = ObjectProperty(lambda x: None)

    # автоматически устанавливаем цвет статуса по строке
    def set_status(self, status: str):
        self.status_text = status.capitalize()
        if status == "sent":
            self.status_color = [0, 1, 0, 1]  # зелёный
        elif status == "error":
            self.status_color = [1, 0, 0, 1]  # красный
        elif status == "scheduled":
            self.status_color = [0, 0, 1, 1]  # синий
        else:
            self.status_color = [0, 0, 0, 1]  # чёрный по умолчанию
