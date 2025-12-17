import os
import shutil
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from contextlib import asynccontextmanager

# Import internal modules
from backend.ingestion import process_file
from backend.vector_store import add_documents_to_store
from backend.rag import query_rag

app = FastAPI(title="Knowledge-Base RAG API")

# Setup directories
UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Knowledge-Base Search Engine API is running"}

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Process and ingest
        chunks = process_file(file_path)
        add_documents_to_store(chunks)
        
        return {"filename": file.filename, "message": "File uploaded and processed successfully"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    try:
        answer, sources = query_rag(request.question)
        return {"answer": answer, "sources": sources}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
