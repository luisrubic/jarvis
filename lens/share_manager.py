class ShareManager:
    def condividi_preferito(self, nome, prezzo, url):
        testo = f"Guarda {nome} - solo {prezzo}€ qui: {url} - trovato con JARVIS"
        print(f"Condivisione: {testo}")
        try:
            from plyer import share
            share.share(text=testo)
        except:
            print(f"[SIMULAZIONE SHARE] {testo}")