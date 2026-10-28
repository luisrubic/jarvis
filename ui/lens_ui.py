from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class LensUI(BoxLayout):
    def __init__(self, camera_manager, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.cm = camera_manager
        self.add_widget(Label(text="LENS V5 - Manda foto in rete e cerca prezzi più bassi", size_hint_y=0.2))
        btn = Button(text="📸 SCATTA E CERCA PREZZO ONLINE", background_color=(0,0.7,1,1), size_hint_y=0.8)
        btn.bind(on_release=lambda x: self.cm.scansiona())
        self.add_widget(btn)