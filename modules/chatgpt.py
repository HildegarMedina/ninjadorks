import os
from openai import OpenAI
from dotenv import load_dotenv
from .agent_ai import AgentAI

load_dotenv()

class ChatGPT(AgentAI):

    def __init__(self, model="gpt-4o-mini-2024-07-18"):
        self.model = model
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate_google_dork(self, description):
        prompt = self._build_prompt(description)
        try:
            result = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )
            return result.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return None
