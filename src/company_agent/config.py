import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str
    ollama_model: str
    ollama_temperature: float


def load_settings() -> Settings:
    return Settings(
        ollama_base_url=os.getenv(
            "OLLAMA_BASE_URL",
            "http://ollama:11434",
        ),
        ollama_model=os.getenv(
            "OLLAMA_MODEL",
            "llama3.2:3b",
        ),
        ollama_temperature=float(
            os.getenv("OLLAMA_TEMPERATURE", "0")
        ),
    )
