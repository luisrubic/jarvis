from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import webbrowser

class ResultsUI:
    def apri(self, nome_prodotto, image_path, risultati_prezzi):
        """
        Mostra popup con risultati dal più economico al più caro
        Ogni riga ha bottone VAI > che apre browser
        """
        print(f"Mostro risultati per {nome_prodotto}")
        
        root = BoxLayout(orientation='vertical', spacing=10, padding=15)
        
        # Titolo
        titolo = Label(
            text=f"[b]{nome_prodotto}[/b]\nTrovato {len(risultati_prezzi)} prezzi - più economico in alto",
            markup=True,
            size_hint_y=0.25,
            halign='center'
        )
        root.add_widget(titolo)
        
        # Scroll prezzi
        scroll = ScrollView(size_hint_y=0.6)
        lista = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        lista.bind(minimum_height=lista.setter('height'))
        
        for i, r in enumerate(risultati_prezzi):
            row = BoxLayout(size_hint_y=None, height=50, spacing=10)
            
            # Highlight più economico
            if i == 0:
                testo = f"[color=00ff00][b]★ {r['store']}: {r['total']}€ (sped incl)[/b][/color]"
            else:
                testo = f"{r['store']}: {r['total']}€"
                
            label = Label(text=testo, markup=True, size_hint_x=0.7, halign='left')
            row.add_widget(label)
            
            btn = Button(
                text="VAI >",
                size_hint_x=0.3,
                background_color=(0, 0.7, 1, 1) if i==0 else (0.5,0.5,0.5,1)
            )
            # Apri link esterno
            btn.bind(on_release=lambda x, url=r['url']: self.apri_link(url))
            row.add_widget(btn)
            
            lista.add_widget(row)
        
        scroll.add_widget(lista)
        root.add_widget(scroll)
        
        # Bottoni chiusura / condividi
        bottoni = BoxLayout(size_hint_y=0.15, spacing=10)
        bottoni.add_widget(Button(text="Chiudi", on_release=lambda x: popup.dismiss()))
        bottoni.add_widget(Button(text="Condividi", on_release=lambda x: self.condividi(nome_prodotto, risultati_prezzi)))
        root.add_widget(bottoni)
        
        popup = Popup(title=f"Prezzi per {nome_prodotto}", content=root, size_hint=(0.95, 0.9))
        popup.open()

    def apri_link(self, url):
        print(f"🌐 Apro browser: {url}")
        webbrowser.open(url)

    def condividi(self, nome, risultati):
        testo = f"Ho trovato {nome} a {risultati[0]['total']}€ su {risultati[0]['store']}\n{risultati[0]['url']}"
        print(f"Share: {testo}")