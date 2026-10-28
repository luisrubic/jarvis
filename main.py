from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from data.settings_manager import SettingsManager
from emergency.chiamata_manager import ChiamataManager
from emergency.sms_gps_manager import SMSGPSManager
from emergency.emergenza_muta import EmergenzaMuta
from emergency.emergenza_parlata import EmergenzaParlata
from core.tts_engine import TTSEngine
from core.wake_word import WakeWordDetector
from lens.product_recognizer import ProductRecognizer
from lens.price_search import PriceSearch
from lens.camera_manager import CameraManager
from economy.receipt_scanner import ReceiptScanner
from economy.expense_categorizer import ExpenseCategorizer
from economy.budget_manager import BudgetManager
from economy.price_db import PriceDB
from economy.comparison_engine import ComparisonEngine
from ui.emergency_ui import EmergencyUI
from ui.settings_ui import SettingsUI
from ui.lens_ui import LensUI
from ui.economy_ui import EconomyUI

class JarvisApp(App):
    def build(self):
        # Init core
        self.settings = SettingsManager()
        self.chiamata = ChiamataManager()
        self.sms = SMSGPSManager()
        self.muta = EmergenzaMuta(self.chiamata, self.sms)
        self.parlata = EmergenzaParlata(self.chiamata, self.sms)
        self.tts = TTSEngine()
        self.wake = WakeWordDetector(self.muta)
        
        # Lens
        self.recognizer = ProductRecognizer()
        self.price_search = PriceSearch()
        self.camera_manager = CameraManager(self.recognizer, self.price_search)
        
        # Economy
        self.price_db = PriceDB()
        self.categorizer = ExpenseCategorizer()
        self.budget = BudgetManager()
        self.comparison = ComparisonEngine(self.price_db)
        self.receipt_scanner = ReceiptScanner(self.categorizer, self.budget, self.comparison)

        # UI Tabs
        tabs = TabbedPanel(do_default_tab=False)
        
        tab1 = TabbedPanelItem(text='SOS')
        tab1.add_widget(EmergencyUI(self.muta, self.parlata))
        tabs.add_widget(tab1)
        
        tab2 = TabbedPanelItem(text='LENS')
        tab2.add_widget(LensUI(self.camera_manager))
        tabs.add_widget(tab2)
        
        tab3 = TabbedPanelItem(text='SPESA')
        tab3.add_widget(EconomyUI(self.receipt_scanner, self.budget))
        tabs.add_widget(tab3)
        
        tab4 = TabbedPanelItem(text='Fidati')
        tab4.add_widget(SettingsUI(self.settings))
        tabs.add_widget(tab4)
        
        # Avvia wake word
        self.wake.start_listening()
        self.tts.parla("Jarvis pronto")
        
        return tabs

if __name__ == '__main__':
    JarvisApp().run()