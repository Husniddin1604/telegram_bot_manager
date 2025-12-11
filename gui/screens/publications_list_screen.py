# gui/screens/publications_list_screen.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.app import App


class PublicationsListScreen(Screen):
    publications = ListProperty([])

    def refresh(self):
        app = App.get_running_app()
        pubs = app.db.get_publications_by_status

        session = app.db.SessionLocal()
        data = session.query(app.db.models.Publication).all()
        session.close()

        self.publications = [
            {
                "id": p.id,
                "title": p.channel.title,
                "status": p.status.value,
                "text": (p.text or "")[:50]
            }
            for p in data
        ]
