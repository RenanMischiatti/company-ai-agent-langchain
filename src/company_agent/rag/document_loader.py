from pathlib import Path

from langchain_core.documents import Document


def load_text_documents(directory: str) -> list[Document]:
    documents_path = Path(directory)

    if not documents_path.exists():
        raise FileNotFoundError(
            f"Diretorio de documentos nao encontrado: {documents_path}"
        )

    documents: list[Document] = []

    for path in sorted(documents_path.glob("*.txt")):
        documents.append(
            Document(
                page_content=path.read_text(encoding="utf-8"),
                metadata={"source": path.name},
            )
        )

    if not documents:
        raise FileNotFoundError(
            f"Nenhum documento .txt encontrado em: {documents_path}"
        )

    return documents
