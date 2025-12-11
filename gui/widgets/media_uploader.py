from kivy.uix.boxlayout import BoxLayout

class MediaUploader(BoxLayout):
    def get_media_path(self):
        return self.ids.filechooser.selection[0] if self.ids.filechooser.selection else None
