import json
import os

class SettingsManager:
    def __init__(self):
        self.path = "data/settings.json"
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.path):
            default = {
                "fidati": [
                    {"nome": "Mamma", "numero": "3330000001", "relazione": "famiglia"},
                    {"nome": "Papà", "numero": "3330000002", "relazione": "famiglia"}
                ],
                "lingua": "it",
                "voce": "it-IT",
                "soglia_db_aiuto": 85,
                "soglia_shake": 2.5
            }
            with open(self.path, 'w') as f:
                json.dump(default, f, indent=2, ensure_ascii=False)
    
    def _load(self):
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except:
            return {"fidati": []}
    
    def _save(self, data):
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ---- FIDATI DINAMICI ----
    def get_fidati(self):
        data = self._load()
        return data.get("fidati", [])

    def add_fidato(self, nome, numero, relazione="fidato"):
        data = self._load()
        # Evita duplicati numero
        data["fidati"] = [f for f in data.get("fidati", []) if f.get("numero") != numero]
        data["fidati"].append({"nome": nome, "numero": numero, "relazione": relazione})
        self._save(data)
        print(f"✅ Fidato aggiunto: {nome} {numero}")
        return data["fidati"]

    def remove_fidato(self, numero):
        data = self._load()
        data["fidati"] = [f for f in data.get("fidati", []) if f.get("numero") != numero]
        self._save(data)
        print(f"🗑️ Fidato rimosso {numero}")
        return data["fidati"]

    def update_fidato(self, vecchio_numero, nuovo_nome, nuovo_numero):
        data = self._load()
        for f in data.get("fidati", []):
            if f.get("numero") == vecchio_numero:
                f["nome"] = nuovo_nome
                f["numero"] = nuovo_numero
        self._save(data)
        return data["fidati"]

    def get_settings(self):
        return self._load()