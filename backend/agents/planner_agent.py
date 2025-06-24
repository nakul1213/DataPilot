 

import pandas as pd
from typing import List
import os
import requests
from dotenv import load_dotenv
load_dotenv()
import time

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")   
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

class PlannerAgent:
    """
    Analyzes the CSV schema and generates a list of data science tasks using Groq LLM.
    """
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)

    def generate_tasks(self) -> List[str]:
        # Analyze the schema
        schema = str(self.df.dtypes)
        prompt = f"""
        Dont add any other text to the response like description of each task just the list of tasks.
        You are a data science workflow planner. Given the following CSV schema:
        {schema}
        Suggest a step-by-step list of 5 tasks (as a Python list of strings) to automate a typical data science pipeline, 
        including data cleaning, EDA, feature engineering,handling imbalances in classes and model training. 
        """
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": "You are an expert data scientist."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 256,
            "temperature": 0.2
        }
        
        time.sleep(2)
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
       
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            
            try:
                tasks = eval(content)
                 
                if isinstance(tasks, list):
                    if len(tasks) > 3:
                        return [str(t) for t in tasks][:3]
                    else:
                        return [str(t) for t in tasks]
                else:
                     
                    return ["EDA","Data Cleaning","Feature Engineering","Model Training","Model Evaluation"]
            except Exception as e:
                print("Error evaluating LLM content:", e)
                print("LLM content was:", content)
                return ["EDA","Data Cleaning","Feature Engineering","Model Training","Model Evaluation"]
            
             
             
        elif response.status_code == 429:
            time.sleep(4)
            response = requests.post(GROQ_API_URL, headers=headers, json=data)
        else:
            raise ValueError(f"Groq API response failed in PlannerAgent with status {response.status_code}: {response.text}") 