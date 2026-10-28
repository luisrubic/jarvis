import threading
import time

class WakeWordDetector:
    def __init__(self, emergenza_muta):
        self.emergenza = emergenza_muta
        self.running = False

    def start_listening(self):
        self.running = True
        threading.Thread(target=self.loop_ascolto, daemon=True).start()
        threading.Thread(target=self.loop_shake, daemon=True).start()
        print("👂 Wake word attivo - ascolto AIUTO >85db")

    def loop_ascolto(self):
        # Su Android usa AudioRecord per db
        while self.running:
            try:
                db = self.get_db_level()  # simulato 70-90
                if db > 85:
                    testo = self.check_word_aiuto()  # STT veloce
                    if "aiuto" in testo.lower():
                        shake = self.get_last_shake()
                        self.emergenza.on_shout_aiuto(db, shake)
            except:
                pass
            time.sleep(0.5)

    def get_db_level(self):
        # TODO: implementa con android.media.MediaRecorder.getMaxAmplitude()
        import random
        return random.randint(60, 95)

    def check_word_aiuto(self):
        # STT leggero per solo "aiuto"
        return "aiuto"

    def get_last_shake(self):
        return 3.0  # simulato, prendi da accelerometro

    def loop_shake(self):
        # plyer.accelerometer
        try:
            from plyer import accelerometer
            accelerometer.enable()
            while self.running:
                val = accelerometer.acceleration
                if val:
                    g = abs(val[0]) + abs(val[1]) + abs(val[2])
                    if g > 2.5:
                        print(f"📳 Scossa {g}G rilevata")
                time.sleep(0.2)
        except:
            pass