-- 08_platform_docs_memory_captures.sql
-- Table used by Firecrawl scheduler (RAG ingest) and platform_docs_search MCP tool.
-- Subject-based chunks with embeddings for semantic search over platform docs.

CREATE TABLE IF NOT EXISTS memory_captures (
    id SERIAL PRIMARY KEY,
    subject TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_memory_captures_subject ON memory_captures(subject);
CREATE INDEX IF NOT EXISTS idx_memory_captures_metadata_url ON memory_captures((metadata->>'url'));
CREATE INDEX IF NOT EXISTS idx_memory_captures_embedding ON memory_captures
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

COMMENT ON TABLE memory_captures IS 'Platform docs RAG: Firecrawl-ingested chunks for platform_docs_search';
