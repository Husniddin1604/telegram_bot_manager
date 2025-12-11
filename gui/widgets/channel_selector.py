from kivy.uix.spinner import Spinner
from kivy.app import App

class ChannelSelector(Spinner):
    def on_parent(self, *_):
        app = App.get_running_app()
        session = app.db.SessionLocal()
        channels = session.query(app.db.models.Channel).all()
        session.close()

        self.values = [c.title for c in channels]
        self._channels = {c.title: c.id for c in channels}

    def get_selected_channel_id(self):
        return self._channels.get(self.text)
