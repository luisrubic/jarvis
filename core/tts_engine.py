from kivy.utils import platform

class TTSEngine:
    def __init__(self):
        self.engine = None
        if platform == 'android':
            try:
                from jnius import autoclass
                Locale = autoclass('java.util.Locale')
                TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                self.tts = TextToSpeech(PythonActivity.mActivity, None)
                self.tts.setLanguage(Locale("it", "IT"))
                self.engine = "android"
                print("TTS Android pronto")
            except Exception as e:
                print(f"TTS errore {e}")
                self.engine = None
        else:
            self.engine = "print"

    def parla(self, testo):
        print(f"🔊 JARVIS: {testo}")
        if self.engine == "android" and hasattr(self, 'tts'):
            try:
                self.tts.speak(testo, 0, None)
            except Exception as e:
                print(f"TTS speak errore {e}")