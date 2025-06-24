 

from dotenv import load_dotenv
load_dotenv()

import nbformat
import os
import requests
import time

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

class OutputGenerator:
    """
    Combines code into a Jupyter notebook and generates a README summary, optionally using Groq LLM for summary.
    """
    def __init__(self):
        pass

    def create_notebook(self, code_blocks, output_path):
        nb = nbformat.v4.new_notebook()
        nb.cells = [nbformat.v4.new_code_cell(code) for code in code_blocks]
        with open(output_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        return output_path

    def create_readme(self, summary, output_path, code_blocks=None):
        # Optionally use LLM to summarize the pipeline
        if code_blocks:
            summary = self.llm_summarize(code_blocks)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Data Science Pipeline Summary\n\n{summary}\n")
        return output_path

    def llm_summarize(self, code_blocks):
        prompt = f"""
You are a data science assistant. Given the following Python code blocks from a data science pipeline, write a concise summary of the steps performed and their purpose.\n\n---\n{chr(10).join(code_blocks)}\n---\nReturn a markdown summary for a README.
"""
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": "You are an expert data science assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 256,
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
            raise ValueError(f"Groq API response failed in OutputGenerator with status {response.status_code}: {response.text}") 