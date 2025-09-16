# DocuRAG – Retrieval‑Augmented Generation for Document Automation

DocuRAG is a **production‑oriented RAG pipeline** featuring:
- **Azure AI Search** for hybrid retrieval (BM25 + vector)
- **Azure OpenAI (GPT-4 / o-series)** for grounded, citation‑backed answers
- **FastAPI** backend with async endpoints
- **Agent‑based workflows** (LangChain) for multi‑step reasoning
- **Evaluation metrics** (BLEU, ROUGE, Recall@K, latency)

> **Note:** This repo includes fully wired code with clear extension points. You must set valid Azure resources and environment variables to run end‑to‑end.

## Features
- 📄 Document ingestion (PDF/DOCX/TXT) → chunking → embedding → Azure AI Search indexing
- 🔍 Hybrid retrieval (keyword + vector) with optional reranking
- 🤖 Agent workflows to plan/search/summarize with tool access
- 📊 Evaluation: BLEU, ROUGE, Recall@K, latency + token/cost tracking
- 🐳 Dockerfile for containerized deployment; works with Azure App Service

## Quickstart

1) **Clone & install**
```bash
git clone https://github.com/<YOUR-USERNAME>/DocuRAG.git
cd DocuRAG
pip install -r requirements.txt
```

2) **Export environment variables**
```bash
export AZURE_SEARCH_ENDPOINT="https://<your-search>.search.windows.net"
export AZURE_SEARCH_KEY="<your-search-admin-key>"
export AZURE_SEARCH_INDEX="docurag-index"

export AZURE_OPENAI_ENDPOINT="https://<your-aoai>.openai.azure.com/"
export AZURE_OPENAI_KEY="<your-aoai-key>"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o-mini"   # or gpt-4o, gpt-35-turbo etc.

# Optional: caching & telemetry
export REDIS_URL="redis://localhost:6379/0"
export DOCURAG_ENABLE_RERANK="true"
```

3) **Run API**
```bash
uvicorn app.main:app --reload
# Open docs: http://127.0.0.1:8000/docs
```

## Endpoints
- `POST /ingest`  – Upload and index documents (`multipart/form-data` file)
- `POST /chat`    – Ask grounded questions: `{ "query": "...", "top_k": 5 }`
- `GET  /evaluate`– Run sample evaluation suite (BLEU/ROUGE/Recall@K)

## Project Structure
```
DocuRAG/
│── app/
│   ├── main.py          # FastAPI entry; routes
│   ├── config.py        # Env config + settings
│   ├── ingestion.py     # Load → chunk → embed → index
│   ├── retrieval.py     # Hybrid search + rerank + prompts
│   ├── agents.py        # LangChain agent orchestration
│   ├── evaluation.py    # Metrics (BLEU/ROUGE/Recall@K/latency)
│   ├── utils.py         # Helpers (chunking, timing, cost)
│── data/                # Sample docs
│── tests/               # Smoke tests
│── requirements.txt
│── Dockerfile
│── .gitignore
│── README.md
```

## Minimal Local Test (No Azure)
You can smoke‑test the server locally without Azure by calling `/health` and using the stubbed retrieval path (it returns sample chunks).

## Production Notes
- Use **Managed Identity** in Azure instead of raw keys where possible.
- For retrieval optimization, consider **scoring profiles** or reranking; you can also plug in a rerank model.
- Add **telemetry**: latency, token usage, cache hit rate.
- Scale via **Azure App Service** or **Azure Functions** (HTTP trigger pointing to `app.main:app`).

