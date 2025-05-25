import requests
from typing import Literal, List

class OllamaClient:
    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434", mode: Literal["generate", "chat"] = "generate"):
        self.model = model
        self.base_url = base_url
        self.mode = mode

    def is_server_running(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/api/tags")
            return r.status_code == 200
        except Exception:
            return False

    def list_models(self) -> List[str]:
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except Exception as e:
            print(f"Error retrieving model list: {e}")
            return []

    def generate(self, prompt: str, max_retries: int = 3) -> str:
        if not self.is_server_running():
            return "[Error] Ollama server is not running. Please start it with 'ollama serve'."

        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json={"model": self.model, "prompt": prompt, "stream": False}
                )
                response.raise_for_status()
                return response.json().get("response", "").strip()
            except Exception as e:
                print(f"Attempt {attempt} failed: {e}")
                if attempt == max_retries:
                    return f"[Error using Ollama after {max_retries} attempts: {e}]"
                continue
