from company_agent.agent.company_agent import CompanyAgent
from company_agent.cli import read_question
from company_agent.config import load_settings
from company_agent.llm.ollama import create_ollama_model


def main() -> None:
    question = read_question()
    settings = load_settings()
    model = create_ollama_model(settings)
    agent = CompanyAgent(model=model)

    response = agent.answer(question)

    print(response)
