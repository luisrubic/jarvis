from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class EconomyUI(BoxLayout):
    def __init__(self, receipt_scanner, budget_manager, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.scanner = receipt_scanner
        self.budget = budget_manager
        
        self.add_widget(Label(text="Economia Famiglia - DOVE/COSA/TOTALE", size_hint_y=0.15))
        
        self.label_report = Label(text="Nessun report ancora", size_hint_y=0.45)
        self.add_widget(self.label_report)
        
        btn_scan = Button(text="🧾 SCANSIONA SCONTRINO", size_hint_y=0.2, background_color=(0,0.7,0,1))
        btn_scan.bind(on_release=self.scansiona)
        self.add_widget(btn_scan)
        
        btn_report = Button(text="📊 REPORT DOVE SPENDI DI PIU'", size_hint_y=0.2)
        btn_report.bind(on_release=self.mostra_report)
        self.add_widget(btn_report)
    
    def scansiona(self, instance):
        dati = self.scanner.scansiona_scontrino()
        self.label_report.text = f"Salvato: {dati['negozio']} - {dati['totale']}€\n{dati['categoria']}"

    def mostra_report(self, instance):
        rep = self.budget.report_mese()
        txt = f"Mese {rep['mese']}: {rep['totale']}€\n"
        for cat, tot in rep['dove_spendi_piu'][:3]:
            txt += f"{cat}: {tot}€\n"
        txt += f"\n{rep['consiglio']}"
        self.label_report.text = txt