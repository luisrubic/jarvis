import os
import datetime

class CameraManager:
    def __init__(self, recognizer, price_search):
        self.recognizer = recognizer
        self.price_search = price_search
        from lens.results_ui import ResultsUI
        self.results_ui = ResultsUI()

    def scansiona(self):
        """Flusso completo: scatta -> manda in rete -> cerca prezzi -> mostra card VAI >"""
        print("📸 Avvio camera")
        path = self.scatta_foto()
        if not path:
            return
            
        # Step 1: Riconosci ONLINE
        nome_prodotto = self.recognizer.riconosci_online(path)
        
        # Step 2: Cerca prezzi ONLINE
        risultati = self.price_search.cerca_tutto_online(nome_prodotto)
        
        # Step 3: Mostra card con VAI >
        self.results_ui.apri(nome_prodotto, path, risultati)

    def scatta_foto(self):
        """Ritorna path foto"""
        # Su Android usa plyer.camera
        try:
            from plyer import camera
            filename = f"/tmp/jarvis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            camera.take_picture(filename=filename, on_complete=lambda x: print(f"Foto salvata {x}"))
            # Per test ritorna file demo
            return "/tmp/test.jpg"
        except:
            print("Camera simulata - usa /tmp/test.jpg")
            return "/tmp/test.jpg"