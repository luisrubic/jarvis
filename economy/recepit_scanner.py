from PIL import Image
import datetime

class ReceiptScanner:
    def __init__(self, categorizer, budget_manager, comparison_engine):
        self.categorizer = categorizer
        self.budget = budget_manager
        self.comparison = comparison_engine

    def scansiona_scontrino(self, image_path="/tmp/scontrino.jpg"):
        print(f"🧾 Scansione scontrino {image_path}")
        
        # Step 1: OCR
        testo_raw = self.ocr(image_path)
        print(f"OCR raw:\n{testo_raw}")
        
        # Step 2: Parse DOVE / COSA / TOTALE
        dati = self.parse_scontrino(testo_raw)
        
        # Step 3: Categoria automatica SPESA/TRASPORTI etc
        categoria = self.categorizer.categorizza_automatica(dati['prodotti'], dati['negozio'])
        dati['categoria'] = categoria
        
        # Step 4: Salva nel budget + price_db
        self.budget.salva_spesa(dati)
        for p in dati['prodotti']:
            self.comparison.price_db.salva_prezzo(p['nome'], dati['negozio'], p['prezzo'])
            
        # Step 5: Confronti risparmio
        confronti = []
        for p in dati['prodotti']:
            c = self.comparison.confronta_prodotto(p['nome'], p['prezzo'], dati['negozio'])
            if c:
                confronti.append(c)
        
        print(f"✅ Scontrino salvato: {dati['negozio']} - {dati['totale']}€ - {categoria}")
        if confronti:
            print("💡 Consigli risparmio:")
            for con in confronti:
                print(f"  - {con}")
        
        return dati

    def ocr(self, image_path):
        try:
            import pytesseract
            img = Image.open(image_path)
            # Lingua italiana
            testo = pytesseract.image_to_string(img, lang='ita')
            return testo
        except Exception as e:
            print(f"OCR errore {e} - uso simulazione")
            return """CONAD AVELLA
27/10/2026 18:32
Prosciutto cotto 100g 3.20
Pasta Barilla 500g 1.90
Pane 1.20
Acqua 0.50
TOTALE 6.80
GRAZIE"""

    def parse_scontrino(self, testo):
        righe = testo.split('\n')
        negozio = "Sconosciuto"
        prodotti = []
        totale = 0.0
        
        # DOVE - prima riga che contiene nome supermercato
        parole_negozi = ['CONAD', 'LIDL', 'CARREFOUR', 'EUROSPIN', 'COOP', 'ESSELUNGA', 'Q8', 'ENI', 'FARMACIA']
        for r in righe[:3]:
            for pn in parole_negozi:
                if pn in r.upper():
                    negozio = r.strip()
                    break
        
        # COSA + PREZZI - righe con numero finale
        for line in righe:
            line = line.strip()
            if not line or 'TOTALE' in line.upper() or 'GRAZIE' in line.upper():
                if 'TOTALE' in line.upper():
                    # Estrai totale
                    try:
                        import re
                        m = re.search(r'(\d+[.,]\d+)', line)
                        if m:
                            totale = float(m.group(1).replace(',', '.'))
                    except:
                        pass
                continue
            
            # Cerca prezzo alla fine: "Prosciutto 3.20"
            import re
            m = re.search(r'(.+?)\s+(\d+[.,]\d+)\s*$', line)
            if m:
                nome = m.group(1).strip()
                try:
                    prezzo = float(m.group(2).replace(',', '.'))
                    if prezzo < 50:  # Evita di prendere date come prezzi
                        prodotti.append({"nome": nome, "prezzo": prezzo})
                except:
                    pass
        
        if totale == 0:
            totale = sum(p['prezzo'] for p in prodotti)
        
        return {
            "negozio": negozio,
            "data": datetime.datetime.now().strftime("%Y-%m-%d"),
            "prodotti": prodotti,
            "totale": totale,
            "testo_raw": testo
        }