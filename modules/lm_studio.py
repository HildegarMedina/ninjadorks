import os
import requests
from dotenv import load_dotenv
from .agent_ai import AgentAI

load_dotenv()

class LmStudio(AgentAI):

    def __init__(self, model="gemma-2-27b-it"):
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
