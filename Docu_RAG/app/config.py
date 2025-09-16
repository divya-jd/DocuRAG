from pydantic import BaseModel
import os

class Settings(BaseModel):
    azure_search_endpoint: str = os.getenv("AZURE_SEARCH_ENDPOINT", "")
    azure_search_key: str = os.getenv("AZURE_SEARCH_KEY", "")
    azure_search_index: str = os.getenv("AZURE_SEARCH_INDEX", "docurag-index")

    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_key: str = os.getenv("AZURE_OPENAI_KEY", "")
    azure_openai_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")

    redis_url: str = os.getenv("REDIS_URL", "")
    enable_rerank: bool = os.getenv("DOCURAG_ENABLE_RERANK", "false").lower() == "true"

settings = Settings()
