from langchain.tools import tool


@tool
def query_company_database(question: str) -> str:
    """Consulta vendas, clientes, pedidos, estoque, faturamento e metricas."""
    return (
        "[SIMULACAO DB] O banco retornou 128 pedidos no mes atual. "
        f"Pergunta consultada: {question}"
    )
