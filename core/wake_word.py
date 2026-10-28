import threading
import time

class WakeWordListener(threading.Thread):
    def __init__(self, assistant):
        super().__init__(daemon=True)
        self.assistant = assistant
        self.running = True
        # Soglie come da tua richiesta
        self.DB_THRESHOLD = 85  # AIUTO urlato
        self.SHAKE_THRESHOLD = 2.5  # Scossa colluttazione

    def run(self):
        print("👂 WakeWord: ascolto sempre JARVIS / AIUTO >85db")
        # Implementazione reale:
        # 1. AudioRecord Android sempre attivo
        # 2. Vosk keyword spotting per "jarvis" "aiuto"
        # 3. Accelerometro per shake_g
        while self.running:
            time.sleep(0.5)
            # simulazione:
            # if self.detect_jarvis(): self.on_detect("JARVIS")
            # if self.detect_aiuto(db, shake): self.on_detect("AIUTO", db, shake)

    def on_detect(self, word, db=90, shake_g=3.0):
        if word == "JARVIS":
            print("🗣️ JARVIS rilevato -> emergenza parlata")
            self.assistant.emergency_parlata.start_flow()
        elif word == "AIUTO":
            print(f"🚨 AIUTO urlato {db}db + shake {shake_g}G -> emergenza muta")
            self.assistant.emergency_muta.on_shout_aiuto(db, shake_g)

    def stop(self):
        self.running = False