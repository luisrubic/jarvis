class ComparisonEngine:
    def __init__(self, price_db):
        self.price_db = price_db

    def confronta_prodotto(self, nome, prezzo_attuale, negozio_attuale):
        """Confronta prezzo attuale con storico famiglia"""
        storico = self.price_db.get_prezzi(nome)
        if not storico or len(storico) < 2:
            return None
        
        # Prezzi precedenti stesso prodotto in altri negozi
        prezzi_altri = [p for p in storico if p['negozio'] != negozio_attuale]
        if not prezzi_altri:
            return None
        
        piu_basso = min(prezzi_altri, key=lambda x: x['prezzo'])
        if prezzo_attuale > piu_basso['prezzo']:
            risparmio = prezzo_attuale - piu_basso['prezzo']
            return f"💡 {nome}: pagato {prezzo_attuale}€ da {negozio_attuale} ma lo avevi preso a {piu_basso['prezzo']}€ da {piu_basso['negozio']} il {piu_basso['data']} - avresti risparmiato {risparmio:.2f}€"
        return None

    def lista_dove_risparmi(self):
        # Analizza tutto lo storico e dice dove risparmi di più
        pass