# backend/main.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from agent_code import main_agent_call, index_pdf  
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

# CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask_question(q: Question):
    try:
        result = main_agent_call(q.question)
        print("Returned from agent:", result)
        return {"answer": result}
    except Exception as e:
        print("Error occurred:", str(e))
        return {"error": str(e)}

@app.post("/upload_pdf")
def upload_pdf(pdf_file: UploadFile = File(...)):
    try:
        # Save uploaded file
        with open("uploaded.pdf", "wb") as f:
            shutil.copyfileobj(pdf_file.file, f)
        
        # Index PDF
        index_pdf("uploaded.pdf")

        return {"status": "PDF uploaded and indexed."}
    except Exception as e:
        print("Error uploading PDF:", str(e))
        return {"error": str(e)}
