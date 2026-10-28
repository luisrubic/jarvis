from data.settings_manager import SettingsManager
from kivy.utils import platform

class ChiamataManager:
    def __init__(self):
        self.settings = SettingsManager()

    def avvia_emergenza_completa(self):
        """Chiama 112 + avvia chiamate a fidati in sequenza"""
        print("📞 Avvio chiamata 112 vivavoce")
        self.chiama_numero("112", vivavoce=True)
        
        # Dopo 5 sec se 112 non risponde, chiama fidati
        # threading.Timer(30, self.chiama_fidati_sequenza).start()

    def chiama_fidati_sequenza(self):
        """Chiama uno ad uno i fidati dinamici presi da settings_manager"""
        fidati = self.settings.get_fidati()
        for f in fidati:
            numero = f.get('numero')
            nome = f.get('nome', 'Fidato')
            print(f"📞 Chiamo fidato {nome} - {numero}")
            self.chiama_numero(numero)
            # Attendi 20 sec prima del prossimo
            import time
            time.sleep(20)

    def chiama_numero(self, numero, vivavoce=True):
        print(f"📞 CHIAMO {numero} - vivavoce={vivavoce}")
        if platform != 'android':
            print(f"[SIMULAZIONE] Chiamata a {numero}")
            return
            
        try:
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            AudioManager = autoclass('android.media.AudioManager')

            # Metti vivavoce
            if vivavoce:
                context = PythonActivity.mActivity.getApplicationContext()
                audio = context.getSystemService(context.AUDIO_SERVICE)
                audio.setSpeakerphoneOn(True)
                audio.setMode(AudioManager.MODE_IN_CALL)

            # Intent chiamata
            intent = Intent()
            intent.setAction(Intent.ACTION_CALL)
            intent.setData(Uri.parse(f"tel:{numero}"))
            PythonActivity.mActivity.startActivity(intent)
            
        except Exception as e:
            print(f"Errore chiamata {numero}: {e} - simulazione attiva")