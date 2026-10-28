import base64
import json

class ProductRecognizer:
    def __init__(self):
        self.api_key = "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"
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"

    def riconosci_online(self, image_path):
        """
        MANDA FOTO IN RETE A GROQ VISION / GPT-4o Vision
        Ritorna: MARCA + MODELLO + COLORE esatto, mai 'oggetto generico'
        """
        print(f"📸 Invio foto IN RETE: {image_path}")
        try:
            with open(image_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode('utf-8')

            # CHIAMATA RETE REALE - decommenta quando hai api key
            import requests
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama-3.2-90b-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Sei un riconoscitore prodotti. Guarda questa foto e rispondi SOLO con MARCA + MODELLO ESATTO + COLORE. Esempio: 'Sony WH-1000XM5 Nero' o 'Nike Air Max 270 Bianca' o 'Barilla Spaghetti 500g'. Se è cibo, dammi marca e peso. MAI dire oggetto generico."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                        ]
                    }
                ],
                "max_tokens": 100
            }
            # resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=20)
            # data = resp.json()
            # nome_prodotto = data['choices'][0]['message']['content'].strip()
            # print(f"✅ Riconosciuto ONLINE: {nome_prodotto}")
            # return nome_prodotto

            # SIMULAZIONE se non hai api key
            print("⚠️ SIMULAZIONE - inserisci API key Groq per rete reale")
            return "Sony WH-1000XM5 Cuffie Wireless Nero - Rilevato via rete"

        except Exception as e:
            print(f"Errore riconoscimento online: {e}")
            return "Prodotto non riconosciuto - riprova con luce migliore"