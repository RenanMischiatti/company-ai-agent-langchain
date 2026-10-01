from langchain_core.embeddings import Embeddings
from langchain_postgres import PGEngine, PGVectorStore

from company_agent.config import Settings


def create_vector_engine(settings: Settings) -> PGEngine:
    return PGEngine.from_connection_string(url=settings.database_url)


def create_vector_store(
    settings: Settings,
    engine: PGEngine,
    embeddings: Embeddings,
) -> PGVectorStore:
    return PGVectorStore.create_sync(
        engine=engine,
        table_name=settings.rag_table_name,
        embedding_service=embeddings,
        id_column="id",
        content_column="content",
        embedding_column="embedding",
        metadata_columns=[
            "document_id",
            "source",
            "section",
            "chunk_index",
            "content_hash",
        ],
        metadata_json_column=None,
    )
