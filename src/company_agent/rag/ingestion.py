from hashlib import sha256
from uuid import NAMESPACE_URL, uuid5

from company_agent.config import load_settings
from company_agent.database.document_repository import synchronize_documents
from company_agent.rag.document_loader import load_text_documents
from company_agent.rag.embeddings import create_embedding_model
from company_agent.rag.section_splitter import split_documents_by_section
from company_agent.rag.vector_store import (
    create_vector_engine,
    create_vector_store,
)


def ingest_documents() -> None:
    settings = load_settings()

    print("Carregando documentos...")
    documents = load_text_documents(settings.rag_documents_path)
    chunks = split_documents_by_section(
        documents=documents,
        chunk_size=settings.rag_chunk_size,
        chunk_overlap=settings.rag_chunk_overlap,
    )

    print(
        f"{len(documents)} documento(s) carregado(s); "
        f"{len(chunks)} chunk(s) produzido(s)."
    )
    print(f"Gerando embeddings com {settings.ollama_embedding_model}...")

    embeddings = create_embedding_model(settings)
    vector_size = len(embeddings.embed_query("dimension probe"))
    if vector_size != settings.rag_embedding_dimension:
        raise ValueError(
            "Dimensao do embedding diferente do schema: "
            f"modelo={vector_size}, schema={settings.rag_embedding_dimension}."
        )

    engine = create_vector_engine(settings)
    vector_store = create_vector_store(
        settings=settings,
        engine=engine,
        embeddings=embeddings,
    )

    document_ids = synchronize_documents(settings, documents)
    for chunk in chunks:
        source = str(chunk.metadata["source"])
        chunk.metadata["document_id"] = document_ids[source]
        chunk.metadata["content_hash"] = sha256(
            chunk.page_content.encode("utf-8")
        ).hexdigest()

    ids = [
        str(
            uuid5(
                NAMESPACE_URL,
                f"{chunk.metadata['document_id']}:"
                f"{chunk.metadata['chunk_index']}:{chunk.page_content}",
            )
        )
        for chunk in chunks
    ]
    vector_store.add_documents(documents=chunks, ids=ids)

    print(f"{len(chunks)} chunk(s) armazenado(s) no PostgreSQL.")
    print("Ingestao concluida.")
