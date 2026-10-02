from company_agent.agent.company_agent import CompanyAgent
from company_agent.agent.prompts import SYSTEM_PROMPT
from company_agent.config import load_settings
from company_agent.llm.ollama import create_ollama_model
from company_agent.agent.tools.factory import create_agent_tools


def create_company_agent() -> CompanyAgent:
    settings = load_settings()
    model = create_ollama_model(settings)
    tools = create_agent_tools(settings)

    return CompanyAgent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )
