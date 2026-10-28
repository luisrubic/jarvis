from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock

class EmergencyUI(BoxLayout):
    def __init__(self, emergenza_muta, emergenza_parlata, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.muta = emergenza_muta
        self.parlata = emergenza_parlata
        
        # Bottone rosso grande
        self.btn_muta = Button(
            text="🚨 EMERGENZA MUTA\nTieni premuto 2 sec",
            font_size=24,
            background_color=(1,0,0,1),
            size_hint_y=0.6
        )
        self.btn_muta.bind(on_press=self.on_press_muta, on_release=self.on_release_muta)
        self.add_widget(self.btn_muta)
        
        self.btn_parlata = Button(
            text="🗣️ EMERGENZA PARLATA",
            background_color=(0,0.5,1,1),
            size_hint_y=0.4
        )
        self.btn_parlata.bind(on_release=lambda x: self.parlata.start_flow())
        self.add_widget(self.btn_parlata)
        
        self.press_time = None

    def on_press_muta(self, instance):
        self.press_time = Clock.get_time()
    
    def on_release_muta(self, instance):
        if self.press_time:
            durata = Clock.get_time() - self.press_time
            if durata >= 2:
                self.muta.conferma_immediata()
            else:
                self.muta.muta_trigger()