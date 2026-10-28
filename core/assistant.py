from emergency.emergenza_muta import EmergenzaMuta
from emergency.emergenza_parlata import EmergenzaParlata
from emergency.chiamata_manager import ChiamataManager
from emergency.sms_gps_manager import SMSGPSManager
from lens.camera_manager import CameraManager
from lens.product_recognizer import ProductRecognizer
from lens.price_search import PriceSearch
from lens.share_manager import ShareManager
from economy.receipt_scanner import ReceiptScanner
from economy.expense_categorizer import ExpenseCategorizer
from economy.budget_manager import BudgetManager
from economy.price_db import PriceDB
from economy.comparison_engine import ComparisonEngine

class JarvisAssistant:
    def __init__(self):
        # EMERGENZA
        self.chiamata = ChiamataManager()
        self.sms_gps = SMSGPSManager()
        self.emergency_muta = EmergenzaMuta(self.chiamata, self.sms_gps)
        self.emergency_parlata = EmergenzaParlata(self.chiamata, self.sms_gps)
        
        # LENS V5 - FOTO IN RETE
        self.recognizer = ProductRecognizer()
        self.price_search = PriceSearch()
        self.share = ShareManager()
        self.lens = CameraManager(self.recognizer, self.price_search)
        
        # ECONOMIA FAMIGLIA
        self.categorizer = ExpenseCategorizer()
        self.budget = BudgetManager()
        self.price_db = PriceDB()
        self.comparison = ComparisonEngine(self.price_db)
        self.economy = ReceiptScanner(self.categorizer, self.budget, self.comparison)

    def load_ui(self):
        # Caricato da main.py
        pass

    def start_wake(self):
        from core.wake_word import WakeWordListener
        wl = WakeWordListener(self)
        wl.start()
        return wl

    def handle_command(self, text):
        t = text.lower()
        if 'emergenza' in t or 'aiuto' in t:
            self.emergency_parlata.start_flow()
        elif 'prodotto' in t or 'cerca' in t or 'quanto costa' in t:
            self.lens.scansiona()
        elif 'scontrino' in t or 'spesa' in t:
            self.economy.scansiona_scontrino()