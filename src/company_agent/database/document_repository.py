from hashlib import sha256
from uuid import NAMESPACE_URL, UUID, uuid5

from langchain_core.documents import Document

from company_agent.config import Settings
from company_agent.database.connection import create_database_connection


def synchronize_documents(
    settings: Settings,
    documents: list[Document],
) -> dict[str, UUID]:
    document_ids: dict[str, UUID] = {}

    with create_database_connection(settings) as connection:
        for document in documents:
            source = str(document.metadata["source"])
            document_id = uuid5(NAMESPACE_URL, source)
            content_hash = sha256(
                document.page_content.encode("utf-8")
            ).hexdigest()

            connection.execute(
                """
                INSERT INTO documents (id, source, content_hash)
                VALUES (%s, %s, %s)
                ON CONFLICT (source) DO UPDATE SET
                    content_hash = EXCLUDED.content_hash,
                    updated_at = NOW()
                """,
                (document_id, source, content_hash),
            )
            connection.execute(
                "DELETE FROM document_chunks WHERE document_id = %s",
                (document_id,),
            )
            document_ids[source] = document_id

    return document_ids
