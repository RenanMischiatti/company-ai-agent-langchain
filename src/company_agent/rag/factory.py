from company_agent.config import Settings
from company_agent.rag.embeddings import create_embedding_model
from company_agent.rag.rag_service import RagService
from company_agent.rag.vector_store import (
    create_vector_engine,
    create_vector_store,
)


def create_rag_service(settings: Settings) -> RagService:
    embeddings = create_embedding_model(settings)
    vector_engine = create_vector_engine(settings)
    vector_store = create_vector_store(
        settings=settings,
        engine=vector_engine,
        embeddings=embeddings,
    )

    return RagService(
        vector_store=vector_store,
        top_k=settings.rag_top_k,
    )
