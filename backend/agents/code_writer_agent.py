# code_writer_agent.py
# Model used: GPT-4

from typing import List
import os
import requests
from dotenv import load_dotenv
import time
import re

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

class CodeWriterAgent:
    """
    Writes Python code for each data science task using Groq LLM.
    """
    def __init__(self):
        pass

    def write_code(self, task: str, context: dict = None) -> str:
        # Compose a prompt for the LLM
        schema_str = ""
        sample_str = ""
        if context:
            if 'csv_schema' in context:
                schema_str = f"\nCSV Schema:\n{context['csv_schema']}"
            if 'csv_sample' in context:
                sample_str = f"\nSample Data (first 3 rows):\n{context['csv_sample']}"
        prompt = f"""
            You are a Python data science expert. Write clean, executable Python code for the following task:
            "{task}"
            If the task is data cleaning or EDA, assume the dataframe is loaded as 'df'.{schema_str}{sample_str}
            Return only the code, no explanations, markdown, or <think> sections. Do not include any text outside of valid Python code.
        """
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": "You are an expert Python data scientist."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2048,
            "temperature": 0.2
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        if response.status_code == 429:
            time.sleep(4)
            response = requests.post(GROQ_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            clean_code = re.sub(r'<think>*?</think>', '', content, flags=re.DOTALL).strip()
            clean_code = clean_code.replace("```python", "").replace("```", "")
            return clean_code 
        else:
            raise ValueError(f"Groq API response failed in CodeWriterAgent with status {response.status_code}: {response.text}") 