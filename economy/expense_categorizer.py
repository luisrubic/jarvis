class ExpenseCategorizer:
    def __init__(self):
        self.keywords = {
            'SPESA': ['prosciutto', 'pasta', 'pane', 'latte', 'uova', 'frutta', 'carne', 'mozzarella', 'barilla', 'yogurt', 'riso', 'tonno', 'pollo', 'mela', 'banana', 'patate', 'formaggio', 'acqua', 'prosciutto cotto', 'cotto', 'pane'],
            'CASA': ['detersivo', 'candeggina', 'scottex', 'spugna', 'sapone', 'ammorbidente'],
            'TRASPORTI': ['benzina', 'gasolio', 'q8', 'eni', 'agip', 'carburante', 'parcheggio'],
            'SALUTE': ['farmacia', 'aspirina', 'tachipirina', 'medicina', 'dottore'],
            'SVAGO': ['birra', 'vino', 'aperitivo', 'cinema', 'pizzeria', 'ristorante'],
            'BOLLETTE': ['enel', 'tim', 'vodafone', 'gas', 'luce', 'bolletta']
        }
        
        self.negozio_to_cat = {
            'CONAD': 'SPESA',
            'LIDL': 'SPESA',
            'CARREFOUR': 'SPESA',
            'EUROSPIN': 'SPESA',
            'COOP': 'SPESA',
            'Q8': 'TRASPORTI',
            'ENI': 'TRASPORTI',
            'AGIP': 'TRASPORTI',
            'FARMACIA': 'SALUTE'
        }

    def categorizza_automatica(self, prodotti, nome_negozio):
        """Come da tua richiesta: PROSCIUTTO COTTO + PASTA BARILLA + PANE -> SPESA"""
        n = nome_negozio.upper()
        
        # 1. Priorità negozio
        for key, cat in self.negozio_to_cat.items():
            if key in n:
                print(f"Categorizzato da negozio {key} -> {cat}")
                return cat
        
        # 2. Priorità prodotti
        for prod in prodotti:
            nome_prod = prod['nome'].lower()
            for cat, parole in self.keywords.items():
                for parola in parole:
                    if parola in nome_prod:
                        print(f"Categorizzato da prodotto '{prod['nome']}' -> {cat}")
                        return cat
        
        # 3. Default SPESA (per CONAD AVELLA)
        return 'SPESA'

    def report_categorie(self, spese):
        """Ritorna dove spendi di più"""
        tot = {}
        for s in spese:
            cat = s.get('categoria', 'ALTRO')
            tot[cat] = tot.get(cat, 0) + s.get('totale', 0)
        return sorted(tot.items(), key=lambda x: x[1], reverse=True)