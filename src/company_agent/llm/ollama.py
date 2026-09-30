from langchain_ollama import ChatOllama

from company_agent.config import Settings


def create_ollama_model(settings: Settings) -> ChatOllama:
    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=settings.ollama_temperature,
    )
