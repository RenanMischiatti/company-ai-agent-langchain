from company_agent.agent.company_agent import CompanyAgent
from company_agent.agent.prompts import SYSTEM_PROMPT
from company_agent.config import load_settings
from company_agent.llm.ollama import create_ollama_model
from company_agent.rag.embeddings import create_embedding_model
from company_agent.rag.rag_service import RagService
from company_agent.rag.vector_store import (
    create_vector_engine,
    create_vector_store,
)
from company_agent.tools.database_query import query_company_database
from company_agent.tools.document_search import create_document_search_tool


def create_company_agent() -> CompanyAgent:
    settings = load_settings()
    model = create_ollama_model(settings)
    embeddings = create_embedding_model(settings)
    vector_engine = create_vector_engine(settings)
    vector_store = create_vector_store(
        settings=settings,
        engine=vector_engine,
        embeddings=embeddings,
    )
    rag_service = RagService(
        vector_store=vector_store,
        top_k=settings.rag_top_k,
    )
    tools = [
        create_document_search_tool(rag_service),
        query_company_database,
    ]

    return CompanyAgent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )
