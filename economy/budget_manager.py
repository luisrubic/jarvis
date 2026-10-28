import json
import os
from datetime import datetime

class BudgetManager:
    def __init__(self):
        self.path = "data/budget.json"
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump({"spese": []}, f)

    def salva_spesa(self, dati_scontrino):
        """Salva DOVE/COSA/TOTALE"""
        try:
            with open(self.path, 'r') as f:
                db = json.load(f)
        except:
            db = {"spese": []}
        
        db["spese"].append(dati_scontrino)
        
        with open(self.path, 'w') as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
        print(f"Spesa salvata {dati_scontrino['totale']}€ in budget.json")

    def get_spese(self, mese=None):
        try:
            with open(self.path, 'r') as f:
                db = json.load(f)
                spese = db.get("spese", [])
        except:
            spese = []
        
        if mese:
            # filtra mese YYYY-MM
            spese = [s for s in spese if s.get('data','').startswith(mese)]
        return spese

    def report_mese(self, mese=None):
        if not mese:
            mese = datetime.now().strftime("%Y-%m")
        
        spese = self.get_spese(mese)
        totale = sum(s.get('totale',0) for s in spese)
        
        # Dove spendi di più
        from economy.expense_categorizer import ExpenseCategorizer
        cat = ExpenseCategorizer()
        per_categoria = cat.report_categorie(spese)
        
        # Per negozio
        per_negozio = {}
        for s in spese:
            n = s.get('negozio','Sconosciuto')
            per_negozio[n] = per_negozio.get(n,0) + s.get('totale',0)
        per_negozio_ord = sorted(per_negozio.items(), key=lambda x: x[1], reverse=True)
        
        report = {
            "mese": mese,
            "totale": totale,
            "num_scontrini": len(spese),
            "dove_spendi_piu": per_categoria,
            "per_negozio": per_negozio_ord,
            "consiglio": self.genera_consiglio(per_categoria, per_negozio_ord)
        }
        
        print(f"REPORT {mese}: Totale {totale}€ - {len(spese)} scontrini")
        for cat, tot in per_categoria:
            print(f"  {cat}: {tot}€")
        print(f"Consiglio: {report['consiglio']}")
        
        return report

    def genera_consiglio(self, per_categoria, per_negozio):
        if not per_categoria:
            return "Nessuna spesa questo mese"
        top_cat = per_categoria[0]
        if top_cat[0] == 'SPESA' and top_cat[1] > 300:
            return f"Spesa alimentare alta ({top_cat[1]}€). Prova LIDL o EUROSPIN per risparmiare ~20%"
        if top_cat[0] == 'TRASPORTI' and top_cat[1] > 150:
            return f"Trasporti {top_cat[1]}€. Confronta prezzi benzina Q8 vs ENI"
        return f"La categoria dove spendi di più è {top_cat[0]}: {top_cat[1]}€"