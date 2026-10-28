import threading
from kivy.utils import platform

class EmergenzaMuta:
    def __init__(self, chiamata_manager, sms_manager):
        self.chiamata = chiamata_manager
        self.sms = sms_manager
        self.shake_threshold = 2.5
        self.db_threshold = 85

    def on_shout_aiuto(self, db_level, shake_g):
        """Chiamato da wake_word.py se AIUTO >85db + scossa >2.5G"""
        print(f"🚨 Rilevato AIUTO {db_level}db + shake {shake_g}G")
        if db_level >= self.db_threshold and shake_g >= self.shake_threshold:
            self.muta_trigger()
        elif db_level >= self.db_threshold:
            # Anche solo urlato forte senza scossa parte
            self.muta_trigger()

    def muta_trigger(self):
        """Bottone rosso o trigger automatico"""
        print("🚨 EMERGENZA MUTA ATTIVATA - Pre-allarme 5s")
        self.vibra(300)
        self.mostra_popup_annulla()
        
        # Timer 5 secondi annullabile
        t = threading.Timer(5.0, self.conferma_sos)
        t.daemon = True
        t.start()
        self.timer = t

    def mostra_popup_annulla(self):
        # UI con bottone ANNULLA grande
        # Se utente preme annulla -> t.cancel()
        print("Popup: Premi ANNULLA entro 5s se falso allarme")

    def annulla(self):
        if hasattr(self, 'timer'):
            self.timer.cancel()
            print("SOS annullato")
            self.vibra(100)

    def vibra(self, ms):
        if platform == 'android':
            try:
                from plyer import vibrator
                vibrator.vibrate(ms / 1000.0)
            except:
                pass

    def conferma_sos(self):
        print("🚨 SOS CONFERMATO - Avvio chiamata + SMS + GPS + registrazione")
        # Ordine come da tua specifica
        self.sms.avvia_sos_completo(tipo_emergenza="AGRESSIONE - EMERGENZA MUTA")
        self.chiamata.avvia_emergenza_completa()

    def conferma_immediata(self):
        """Se utente tiene premuto 2 sec"""
        if hasattr(self, 'timer'):
            self.timer.cancel()
        self.conferma_sos()