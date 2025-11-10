from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from .ingest import ingest_files
from .retriever import build_qa_chain
from .config import settings
import shutil

app = FastAPI(title="RAG Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/ingest")
async def ingest_endpoint(files: List[UploadFile] = File(...)):
    """
    Upload one or more documents to be ingested into the vector store.
    Supported: .txt, .pdf (UnstructuredPDFLoader)
    """
    tmp_dir = "/tmp/rag_uploads"
    os.makedirs(tmp_dir, exist_ok=True)
    saved_paths = []
    try:
        for file in files:
            file_path = os.path.join(tmp_dir, file.filename)
            with open(file_path, "wb") as f:
                contents = await file.read()
                f.write(contents)
            saved_paths.append(file_path)
        count = ingest_files(saved_paths, persist_directory=settings.chroma_persist_directory)
        # clean up uploaded files
        for p in saved_paths:
            try:
                os.remove(p)
            except:
                pass
        return {"status": "ok", "chunks_indexed": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_endpoint(query: Query):
    """
    Query the RAG system. Returns answer text + sources.
    """
    try:
        qa_chain = build_qa_chain()
        result = qa_chain({"query": query.question})
        # langchain versions vary: prefer keys 'result' or 'answer'
        answer = result.get("result") or result.get("answer") or ""
        docs = result.get("source_documents", []) or result.get("source_documents", [])
        sources = []
        for d in docs:
            metadata = getattr(d, "metadata", {})
            page_content = getattr(d, "page_content", str(d))[:1000]
            sources.append({"page_content": page_content, "metadata": metadata})
        return {"answer": answer, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}
