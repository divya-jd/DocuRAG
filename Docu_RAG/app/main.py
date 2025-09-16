from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from .ingestion import ingest_bytes
from .retrieval import retrieve, generate_answer
from .agents import agent_chat
from .evaluation import bleu_score, rouge_l, recall_at_k

app = FastAPI(title="DocuRAG", version="0.1.0")

class ChatRequest(BaseModel):
    query: str
    top_k: int = 5
    agent: bool = True

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    data = await file.read()
    docs = ingest_bytes(file.filename, data)
    return {"indexed": len(docs), "preview": docs[:2]}

@app.post("/chat")
async def chat(req: ChatRequest):
    if req.agent:
        result = agent_chat(req.query)
        return result
    docs = retrieve(req.query, top_k=req.top_k)
    answer, used = generate_answer(docs, req.query)
    return {"answer": answer, "citations": used}

@app.get("/evaluate")
async def evaluate():
    refs = ["Azure AI Search and Azure OpenAI enable RAG with hybrid retrieval."]
    hyps = ["Azure OpenAI and AI Search provide hybrid RAG."]
    return {
        "bleu": bleu_score(refs, hyps),
        "rougeL": rouge_l(refs, hyps),
        "recall@5_example": recall_at_k(["doc-1"], ["doc-1", "doc-2", "doc-3"], k=5),
    }
