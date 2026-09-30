import argparse


def read_question() -> str:
    parser = argparse.ArgumentParser(
        prog="company_agent",
        description="Envia uma pergunta para o agente empresarial.",
    )
    parser.add_argument(
        "question",
        nargs="+",
        help="Pergunta que sera enviada ao agente.",
    )

    arguments = parser.parse_args()
    question = " ".join(arguments.question).strip()

    if not question:
        parser.error("a pergunta nao pode estar vazia")

    return question
