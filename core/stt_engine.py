class STTEngine:
    def __init__(self):
        pass

    def listen(self, timeout=5):
        """Ritorna testo ascoltato - 5 sec"""
        print(f"🎤 Ascolto {timeout}s...")
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=timeout, phrase_time_limit=timeout)
                testo = r.recognize_google(audio, language="it-IT")
                print(f"Riconosciuto: {testo}")
                return testo
        except Exception as e:
            print(f"STT simulazione - errore {e}")
            # Simulazione per test su PC senza mic
            return input("Scrivi cosa dici (simulazione STT): ") or "auto"