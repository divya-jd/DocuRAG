from typing import List, Dict
from .utils import chunk_text
import os

# NOTE: wire to Azure AI Search SDK in production.
# Here we simply return chunked text; in prod, you create/update the index and upload docs.

def ingest_bytes(name: str, data: bytes) -> List[Dict]:
    text = data.decode('utf-8', errors='ignore')
    chunks = chunk_text(text, max_tokens=180)
    docs = [{"id": f"{name}-{i}", "content": c} for i, c in enumerate(chunks)]
    # TODO: push 'docs' into Azure AI Search index
    return docs
