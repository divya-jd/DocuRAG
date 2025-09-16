from typing import List, Dict, Tuple
from .utils import sample_docs
from .config import settings
from openai import OpenAI

# Simplified retrieval + LLM. Replace retrieval with Azure AI Search SDK calls in production.

def retrieve(query: str, top_k: int = 5) -> List[Dict]:
    docs = sample_docs()
    # naive scoring: rank by overlapping words
    scored = []
    q_words = set(query.lower().split())
    for d in docs:
        score = len(q_words.intersection(set(d["content"].lower().split())))
        scored.append((score, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_k]]

def generate_answer(context_docs: List[Dict], query: str) -> Tuple[str, List[Dict]]:
    context = "\n\n".join([f"[{d['id']}] {d['content']}" for d in context_docs])
    prompt = f"""You are a helpful assistant. Use the CONTEXT to answer the QUESTION.
Cite sources by their [id].
CONTEXT:
{context}

QUESTION: {query}
"""
    if settings.azure_openai_endpoint and settings.azure_openai_key:
        client = OpenAI(
            base_url=f"{settings.azure_openai_endpoint}openai/deployments/{settings.azure_openai_deployment}/",
            api_key=settings.azure_openai_key,
        )
        # The 'openai' python package uses 'client.chat.completions.create' for chat models
        # When using Azure OpenAI via the official OpenAI SDK, ensure 'base_url' matches AOAI.
        resp = client.chat.completions.create(
            model=settings.azure_openai_deployment,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        text = resp.choices[0].message.content
    else:
        # Offline stub:
        text = "Based on the retrieved docs, Azure AI Search + Azure OpenAI with FastAPI enables RAG."
    return text, context_docs
