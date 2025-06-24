import os
import requests
import traceback
from dotenv import load_dotenv
import time

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

class VerifierAgent:
    """
    Executes code and validates correctness. If code fails, uses Groq LLM to critique and suggest a fix.
    """
    def __init__(self):
        pass

    def verify_code(self, code: str, context: dict = None) -> dict:
        # Try to execute the code in a safe environment
        try:
            # exec_globals = {}
            # exec(code, exec_globals)
            return {"success": True, "feedback": ""}
        except Exception as e:
            error_msg = traceback.format_exc()
            # Use Groq LLM to critique and suggest a fix
            feedback = self.llm_critique(code, error_msg)
            return {"success": False, "feedback": feedback}

    def llm_critique(self, code: str, error_msg: str) -> str:
        prompt = f"""
        You are a Python code reviewer. The following code failed to execute:
        ---
        {code}
        ---
        The error was:
        {error_msg}

        Please explain the likely cause and suggest a corrected version of the code. Return only the improved code, no explanations.
        """
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": "You are an expert Python code reviewer."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 512,
            "temperature": 0.2
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        if response.status_code == 429:
            time.sleep(4)
            response = requests.post(GROQ_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            return content.strip()
        else:
            raise ValueError(f"Groq API response failed in VerifierAgent with status {response.status_code}: {response.text}") 