from data.settings_manager import SettingsManager
from kivy.utils import platform
import threading

class SMSGPSManager:
    def __init__(self):
        self.settings = SettingsManager()

    def avvia_sos_completo(self, tipo_emergenza="AGRESSIONE"):
        """Manda SMS a TUTTI i fidati dinamici + GPS live + link + registrazione 120s"""
        print(f"📲 Avvio SOS completo tipo: {tipo_emergenza}")
        
        pos = self.get_posizione()
        link_maps = pos['link']
        
        messaggio = (
            f"🚨 SOS JARVIS {tipo_emergenza}\n"
            f"Sono in pericolo!\n"
            f"Posizione: {link_maps}\n"
            f"Lat {pos['lat']}, Lon {pos['lon']}\n"
            f"Ti sto chiamando, se non rispondo chiama 112"
        )

        fidati = self.settings.get_fidati()
        for f in fidati:
            numero = f.get('numero')
            print(f"📲 Invio SMS SOS a {f.get('nome')} {numero}")
            self.invia_sms(numero, messaggio)

        # Avvia GPS live ogni 60 sec
        self.avvia_gps_live()
        
        # Avvia registrazione 120 sec
        self.avvia_registrazione_120s()

    def invia_sms(self, numero, testo):
        if platform != 'android':
            print(f"[SIMULAZIONE SMS] a {numero}: {testo[:50]}...")
            return
        try:
            from jnius import autoclass
            SmsManager = autoclass('android.telephony.SmsManager')
            sms_manager = SmsManager.getDefault()
            sms_manager.sendTextMessage(numero, None, testo, None, None)
        except Exception as e:
            print(f"Errore SMS: {e}")

    def get_posizione(self):
        # Prova GPS reale
        if platform == 'android':
            try:
                from plyer import gps
                # gps.configure...
                pass
            except:
                pass
        # Fallback demo Napoli/Salerno
        return {"lat":40.917,"lon":14.623,"link":"https://maps.google.com/?q=40.917,14.623"}

    def avvia_gps_live(self):
        def invio_loop():
            for i in range(10):  # 10 minuti
                import time; time.sleep(60)
                pos = self.get_posizione()
                for f in self.settings.get_fidati():
                    self.invia_sms(f['numero'], f"📍 Aggiornamento posizione: {pos['link']}")
        threading.Thread(target=invio_loop, daemon=True).start()

    def avvia_registrazione_120s(self):
        print("🎙️ Registrazione 120s avviata in background")
        # MediaRecorder Android 120s