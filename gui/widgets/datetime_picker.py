from kivy.uix.boxlayout import BoxLayout
from datetime import datetime

class DateTimePicker(BoxLayout):
    def get_datetime(self):
        date = self.ids.date_input.text
        time = self.ids.time_input.text
        try:
            return datetime.fromisoformat(f"{date} {time}")
        except:
            return None
