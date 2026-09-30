from company_agent.agent.company_agent import CompanyAgent
from company_agent.agent.prompts import SYSTEM_PROMPT
from company_agent.config import load_settings
from company_agent.llm.ollama import create_ollama_model
from company_agent.tools.database_query import query_company_database
from company_agent.tools.document_search import search_internal_documents


def create_company_agent() -> CompanyAgent:
    settings = load_settings()
    model = create_ollama_model(settings)
    tools = [
        search_internal_documents,
        query_company_database,
    ]

    return CompanyAgent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )
