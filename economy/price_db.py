import json
import os
from datetime import datetime

class PriceDB:
    def __init__(self):
        self.path = "data/prices.json"
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump({}, f)

    def salva_prezzo(self, nome_prodotto, negozio, prezzo):
        """Storico prezzi famiglia"""
        try:
            with open(self.path, 'r') as f:
                db = json.load(f)
        except:
            db = {}
        
        key = nome_prodotto.lower().strip()
        if key not in db:
            db[key] = []
        
        db[key].append({
            "negozio": negozio,
            "prezzo": prezzo,
            "data": datetime.now().strftime("%Y-%m-%d")
        })
        
        with open(self.path, 'w') as f:
            json.dump(db, f, indent=2, ensure_ascii=False)

    def get_prezzi(self, nome_prodotto):
        try:
            with open(self.path, 'r') as f:
                db = json.load(f)
                return db.get(nome_prodotto.lower().strip(), [])
        except:
            return []