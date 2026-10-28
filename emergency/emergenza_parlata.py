from core.tts_engine import TTSEngine
from core.stt_engine import STTEngine

class EmergenzaParlata:
    def __init__(self, chiamata_manager, sms_manager):
        self.chiamata = chiamata_manager
        self.sms = sms_manager
        self.tts = TTSEngine()
        self.stt = STTEngine()
        self.tipo = None

    def start_flow(self):
        """Flow: JARVIS -> che emergenza? -> auto/manuale?"""
        print("🗣️ Avvio flow emergenza parlata")
        
        # Step 1: Che emergenza?
        self.tts.parla("Che emergenza? Aggressione, medica o furto?")
        tipo_risposta = self.stt.listen(timeout=5)
        self.tipo = self.classifica_tipo(tipo_risposta)
        print(f"Tipo rilevato: {self.tipo}")

        # Step 2: Auto o manuale?
        self.tts.parla("Chiamo io o chiami tu? Di auto o manuale")
        modo_risposta = self.stt.listen(timeout=5)
        
        if "auto" in modo_risposta.lower() or "tu" in modo_risposta.lower() or modo_risposta == "":
            # JARVIS chiama
            self.tts.parla(f"Ok, chiamo io, emergenza {self.tipo}, mando SMS ai tuoi fidati")
            self.sms.avvia_sos_completo(tipo_emergenza=self.tipo)
            self.chiamata.avvia_emergenza_completa()
        else:
            # Manuale - attiva solo muta con bottone
            self.tts.parla("Ok, tieni premuto il bottone rosso due secondi se hai bisogno, io resto qui")

    def classifica_tipo(self, testo):
        t = testo.lower()
        if "aggress" in t or "picchi" in t or "uomo" in t:
            return "AGRESSIONE"
        elif "medic" in t or "male" in t or "aiuto" in t or "cuore" in t:
            return "MEDICA"
        elif "furto" in t or "ladro" in t or "rub" in t:
            return "FURTO"
        else:
            return "AGRESSIONE - GENERICA"