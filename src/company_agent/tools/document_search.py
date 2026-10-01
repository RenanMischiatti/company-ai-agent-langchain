from langchain_core.tools import BaseTool
from langchain.tools import tool

from company_agent.rag.rag_service import RagService


def create_document_search_tool(rag_service: RagService) -> BaseTool:
    @tool
    def search_internal_documents(question: str) -> str:
        """Pesquisa politicas, normas, manuais, beneficios e processos internos."""
        return rag_service.search(question)

    return search_internal_documents
