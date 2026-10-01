CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY,
    source TEXT NOT NULL UNIQUE,
    content_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID PRIMARY KEY,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding VECTOR(768) NOT NULL,
    source TEXT NOT NULL,
    section TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    content_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (document_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS document_chunks_document_id_idx
    ON document_chunks (document_id);

CREATE INDEX IF NOT EXISTS document_chunks_embedding_hnsw_idx
    ON document_chunks
    USING hnsw (embedding vector_cosine_ops);
