from typing import Dict, List
from .retrieval import retrieve, generate_answer

# Minimal 'agent-like' planner: decide to retrieve, then answer.
# In production, use LangChain Agents or Semantic Kernel with tools.

def agent_chat(query: str) -> Dict:
    plan = [
        {"step": "retrieve", "args": {"query": query}},
        {"step": "answer", "args": {"query": query}},
    ]
    docs = retrieve(query, top_k=5)
    answer, used = generate_answer(docs, query)
    return {"plan": plan, "answer": answer, "citations": used}
