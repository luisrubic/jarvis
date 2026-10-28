from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class SettingsUI(BoxLayout):
    def __init__(self, settings_manager, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.sm = settings_manager
        
        self.add_widget(Label(text="Fidati dinamici - aggiungi/rimuovi", size_hint_y=0.1))
        
        # Form aggiunta
        form = BoxLayout(size_hint_y=0.2, spacing=5)
        self.input_nome = TextInput(hint_text="Nome", size_hint_x=0.4)
        self.input_numero = TextInput(hint_text="Numero 333...", size_hint_x=0.4)
        btn_add = Button(text="Aggiungi", size_hint_x=0.2, on_release=self.add_fidato)
        form.add_widget(self.input_nome)
        form.add_widget(self.input_numero)
        form.add_widget(btn_add)
        self.add_widget(form)
        
        # Lista
        self.scroll = ScrollView(size_hint_y=0.7)
        self.lista_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.lista_box.bind(minimum_height=self.lista_box.setter('height'))
        self.scroll.add_widget(self.lista_box)
        self.add_widget(self.scroll)
        
        self.refresh_lista()

    def refresh_lista(self):
        self.lista_box.clear_widgets()
        for f in self.sm.get_fidati():
            row = BoxLayout(size_hint_y=None, height=40, spacing=5)
            row.add_widget(Label(text=f"{f['nome']} - {f['numero']}", size_hint_x=0.7))
            btn_del = Button(text="X", size_hint_x=0.3, background_color=(1,0,0,1))
            btn_del.bind(on_release=lambda x, num=f['numero']: self.del_fidato(num))
            row.add_widget(btn_del)
            self.lista_box.add_widget(row)

    def add_fidato(self, instance):
        nome = self.input_nome.text.strip()
        numero = self.input_numero.text.strip()
        if nome and numero:
            self.sm.add_fidato(nome, numero)
            self.input_nome.text = ""
            self.input_numero.text = ""
            self.refresh_lista()

    def del_fidato(self, numero):
        self.sm.remove_fidato(numero)
        self.refresh_lista()