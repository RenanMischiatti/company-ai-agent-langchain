from company_agent.bootstrap import create_company_agent
from company_agent.cli import read_question


def main() -> None:
    question = read_question()
    agent = create_company_agent()
    response = agent.answer(question)

    print(response)
