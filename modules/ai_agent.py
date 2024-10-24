import os
import requests
from dotenv import load_dotenv

load_dotenv()

class IAAgent:

    def __init__(self, model="llama-3.2-3b-instruct"):
        self.base_url = os.environ.get("LM_STUDIO_BASE_URL")
        self.model = model

    def request_chat_completions(self, prompt):
        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
        }
        body = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }
        response = requests.post(url, headers=headers, json=body)
        return response.json()

    def generate_google_dork(self, description):
        prompt = self._build_prompt(description)
        try:
            result = self.request_chat_completions(prompt)
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error: {e}")
            return None

    def _build_prompt(self, description):
        return f"""
            Genera un Google Dork específico basado en la descripción del usuario. Un Google Dork utiliza operadores avanzados en motores de búsqueda para encontrar información específica que es difícil de encontrar mediante una búsqueda normal. Tu tarea es convertir la descripción del usuario en un Google Dork preciso. A continuación, se presentan algunos ejemplos de cómo deberías formular los Google Dorks basándote en diferentes descripciones:

            Descripción: Documentos PDF relacionados con la seguridad informática publicados en el último año.
            Google Dork: filetype:pdf "seguridad informática" after:2023-01-01

            Descripción: Presentaciones de Powerpoint sobre cambio climático disponibles en sitios .edu.
            Google Dork: site:.edu filetype:ppt "cambio climático"

            Descripción: Listas de correos electrónicos en archivos de texto dentro de dominios gubernamentales.
            Google Dork: site:.gov filetype:txt "email" | "correo electrónico"

            Ahora, basado en la siguiente descripción proporcionada por el usuario, genera el Google Dork correspondiente:

            Descripción: {description}
        """

if __name__ == "__main__":
    ia_agent = IAAgent()
    description = "PDF que contienen el nombre Hildegar Medina con exactitud"
    print(ia_agent.generate_google_dork(description))
