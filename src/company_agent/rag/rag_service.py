from langchain_core.vectorstores import VectorStore


class RagService:
    def __init__(self, vector_store: VectorStore, top_k: int) -> None:
        self._vector_store = vector_store
        self._top_k = top_k

    def search(self, question: str) -> str:
        documents = self._vector_store.similarity_search(
            question,
            k=self._top_k,
        )

        if not documents:
            return "Nenhuma informacao foi encontrada nos documentos internos."

        contexts = []
        for document in documents:
            source = document.metadata.get("source", "desconhecida")
            section = document.metadata.get("section", "sem secao")
            contexts.append(
                f"Fonte: {source}\nSecao: {section}\n{document.page_content}"
            )

        return "\n\n---\n\n".join(contexts)
