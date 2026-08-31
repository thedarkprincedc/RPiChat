import requests
import json

class OllamaService:
    def __init__(self, ollama_base_url):
        self.ollama_base_url = ollama_base_url

    def test_connection(self):
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Connection failed: {e}")
            return False

    def generate_text(self, prompt, model="llama3.2"):
        response = requests.post(
            f"{self.ollama_base_url}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )
        return response.json()["response"]

    def generate_text_stream(self, prompt, model="llama3.2"):
        response = requests.post(
            f"{self.ollama_base_url}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            stream=True
        )

        response.raise_for_status()
        
        for line in response.iter_lines():
            if not line:
                continue

            data = json.loads(line)
            
            print(data)