from langchain.tools import tool


@tool
def search_internal_documents(question: str) -> str:
    """Pesquisa politicas, normas, manuais, beneficios e processos internos."""
    return (
        "[SIMULACAO RAG] A politica interna de ferias permite 30 dias "
        "de descanso apos cada periodo aquisitivo de 12 meses. "
        f"Pergunta consultada: {question}"
    )
