import time
from typing import List, Dict

def chunk_text(text: str, max_tokens: int = 500) -> List[str]:
    # naive chunker by sentences; replace with tiktoken-aware chunking in prod
    parts = []
    buf = []
    count = 0
    for sent in text.split('. '):
        buf.append(sent)
        count += len(sent.split())
        if count >= max_tokens:
            parts.append('. '.join(buf).strip())
            buf, count = [], 0
    if buf:
        parts.append('. '.join(buf).strip())
    return parts

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start

def cost_tracker(tokens_in: int, tokens_out: int, cost_per_1k_in=0.005, cost_per_1k_out=0.015) -> float:
    return (tokens_in/1000.0)*cost_per_1k_in + (tokens_out/1000.0)*cost_per_1k_out

def sample_docs() -> List[Dict]:
    return [
        {"id": "1", "content": "Azure AI Search enables powerful hybrid retrieval with BM25 and vector search."},
        {"id": "2", "content": "Azure OpenAI provides GPT models that can ground responses using retrieved context."},
        {"id": "3", "content": "FastAPI is a high performance Python web framework ideal for async inference."},
    ]
