import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str
    ollama_model: str
    ollama_temperature: float
    ollama_embedding_model: str
    database_url: str
    rag_documents_path: str
    rag_table_name: str
    rag_embedding_dimension: int
    rag_chunk_size: int
    rag_chunk_overlap: int
    rag_top_k: int


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
        ollama_embedding_model=os.getenv(
            "OLLAMA_EMBEDDING_MODEL",
            "nomic-embed-text-v2-moe",
        ),
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://company:company@postgres:5432/company",
        ),
        rag_documents_path=os.getenv(
            "RAG_DOCUMENTS_PATH",
            "/app/data/documents",
        ),
        rag_table_name=os.getenv(
            "RAG_TABLE_NAME",
            "document_chunks",
        ),
        rag_embedding_dimension=int(
            os.getenv("RAG_EMBEDDING_DIMENSION", "768")
        ),
        rag_chunk_size=int(os.getenv("RAG_CHUNK_SIZE", "1200")),
        rag_chunk_overlap=int(os.getenv("RAG_CHUNK_OVERLAP", "150")),
        rag_top_k=int(os.getenv("RAG_TOP_K", "4")),
    )
