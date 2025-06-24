from pydantic import BaseModel
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from uuid import uuid4
import time
from langgraph_flow import run_pipeline
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()
app = FastAPI()
UPLOAD_DIR = "uploads"

from fastapi.staticfiles import StaticFiles
import os

# Mount the outputs directory
OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "outputs")
app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR), name="outputs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UploadResponse(BaseModel):
    file_id: str
    filename: str

class RunRequest(BaseModel):
    file_id: str

class RunResponse(BaseModel):
    notebook: str
    readme: str
    summary: str

@app.post("/upload", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return {"file_id": file_id, "filename": file.filename}

@app.post("/run", response_model=RunResponse)
async def run_pipeline_endpoint(request: RunRequest):
    file_id = request.file_id
    # Find the uploaded CSV file by file_id
    for fname in os.listdir(UPLOAD_DIR):
        if fname.startswith(file_id):
            csv_path = os.path.join(UPLOAD_DIR, fname)
           
            break
    else:
        raise HTTPException(status_code=404, detail="CSV file not found.")
    # Run the agentic pipeline
   
    result = run_pipeline(csv_path)
    return {
        "notebook": result.get("notebook", ""),
        "readme": result.get("readme", ""),
        "summary": result.get("summary", ""),
    } 