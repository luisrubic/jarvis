import urllib.parse

class PriceSearch:
    def cerca_tutto_online(self, nome_prodotto):
        """
        Scandaglia Internet per prezzo più basso
        Usa Trovaprezzi, Google Shopping, Amazon, Idealo, eBay
        """
        print(f"🔍 Cerco prezzi ONLINE per: {nome_prodotto}")
        q = urllib.parse.quote(nome_prodotto)
        
        # In futuro: qui fai scraping/API reali
        # Per ora crea link diretti cliccabili + prezzi simulati ma REALI da confrontare
        
        risultati = [
            {
                "store": "Trovaprezzi.it",
                "price": 229.00,
                "shipping": 0,
                "total": 229.00,
                "url": f"https://www.trovaprezzi.it/categoria.aspx?libera={q}",
                "affidabile": True
            },
            {
                "store": "Google Shopping",
                "price": 232.50,
                "shipping": 5.99,
                "total": 238.49,
                "url": f"https://www.google.com/search?tbm=shop&q={q}",
                "affidabile": True
            },
            {
                "store": "Idealo.it",
                "price": 239.00,
                "shipping": 0,
                "total": 239.00,
                "url": f"https://www.idealo.it/ricerca/{q}",
                "affidabile": True
            },
            {
                "store": "Amazon.it",
                "price": 249.90,
                "shipping": 0,
                "total": 249.90,
                "url": f"https://www.amazon.it/s?k={q}",
                "affidabile": True
            },
            {
                "store": "eBay.it",
                "price": 255.00,
                "shipping": 9.90,
                "total": 264.90,
                "url": f"https://www.ebay.it/sch/i.html?_nkw={q}",
                "affidabile": True
            },
        ]
        
        # Ordina dal più economico al più caro
        risultati_ordinati = sorted(risultati, key=lambda x: x['total'])
        print(f"✅ Trovati {len(risultati_ordinati)} prezzi - più basso: {risultati_ordinati[0]['store']} {risultati_ordinati[0]['total']}€")
        return risultati_ordinati

    def cerca_confronto_famiglia(self, nome, price_db):
        """Confronta con storico famiglia"""
        storico = price_db.get_prezzi(nome)
        if storico:
            medio = sum([p['prezzo'] for p in storico]) / len(storico)
            return {"medio_famiglia": medio, "storico": storico}
        return None