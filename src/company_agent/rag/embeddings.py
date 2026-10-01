from langchain_ollama import OllamaEmbeddings

from company_agent.config import Settings


def create_embedding_model(settings: Settings) -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=settings.ollama_embedding_model,
        base_url=settings.ollama_base_url,
    )
