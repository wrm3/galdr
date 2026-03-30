-- ============================================================
-- 02_schema.sql
-- Core RAG schema for galdr
-- ============================================================
-- Run order: 02 (after extensions)
-- Purpose: Create tables, indexes, and functions for RAG storage
-- Supports: YouTube, Webpages, GitHub, PDFs, Images, Documents
-- ============================================================

-- ============================================================
-- Table: sources
-- Unified source table for all content types
-- ============================================================
CREATE TABLE IF NOT EXISTS sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Source identification
    source_type TEXT NOT NULL,          -- 'youtube', 'webpage', 'github', 'pdf', 'image', 'document', 'text'
    source_id TEXT NOT NULL,            -- Unique ID within type (video_id, URL hash, file hash)
    url TEXT,                           -- Original URL if applicable
    file_path TEXT,                     -- Local file path if applicable

    -- Content metadata
    title TEXT NOT NULL,
    author TEXT,
    description TEXT,
    content_full TEXT,                  -- Full extracted text content

    -- Type-specific metadata (flexible JSON)
    metadata JSONB DEFAULT '{}',

    -- Processing status
    status TEXT DEFAULT 'pending',      -- 'pending', 'processing', 'completed', 'failed'
    error_message TEXT,

    -- Timestamps
    source_created_at TIMESTAMP,        -- When original content was created
    processed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT unique_source UNIQUE(source_type, source_id)
);

-- Indexes for sources
CREATE INDEX IF NOT EXISTS idx_sources_type ON sources(source_type);
CREATE INDEX IF NOT EXISTS idx_sources_status ON sources(status);
CREATE INDEX IF NOT EXISTS idx_sources_url ON sources(url);
CREATE INDEX IF NOT EXISTS idx_sources_created ON sources(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_sources_title_trgm ON sources USING gin(title gin_trgm_ops);

-- ============================================================
-- Table: content_chunks
-- Text chunks with embeddings for semantic search
-- ============================================================
CREATE TABLE IF NOT EXISTS content_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,

    -- Chunk content
    chunk_text TEXT NOT NULL,
    chunk_index INT NOT NULL,           -- Order within source (0-based)
    chunk_type TEXT NOT NULL,           -- 'text', 'code', 'heading', 'list', 'table', 'image_caption'

    -- Position in source (flexible based on type)
    position_start DECIMAL,             -- Start position (timestamp for video, char offset for text)
    position_end DECIMAL,               -- End position
    position_metadata JSONB,            -- Type-specific: {page: 5}, {section: "intro"}, etc.

    -- Embedding (OpenAI text-embedding-3-small = 1536 dimensions)
    embedding VECTOR(1536),

    -- Stats
    word_count INT,
    char_count INT,

    -- Flags
    has_code BOOLEAN DEFAULT FALSE,
    has_table BOOLEAN DEFAULT FALSE,
    has_image BOOLEAN DEFAULT FALSE,

    -- Metadata
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT unique_source_chunk UNIQUE(source_id, chunk_index)
);

-- HNSW index for semantic search (better than IVFFlat for most use cases)
-- Uses cosine similarity (most common for OpenAI embeddings)
CREATE INDEX IF NOT EXISTS idx_content_chunks_embedding ON content_chunks
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS idx_content_chunks_source ON content_chunks(source_id);
CREATE INDEX IF NOT EXISTS idx_content_chunks_type ON content_chunks(chunk_type);
CREATE INDEX IF NOT EXISTS idx_content_chunks_text_trgm ON content_chunks USING gin(chunk_text gin_trgm_ops);

-- ============================================================
-- Table: search_history
-- Track search queries for analytics and caching
-- ============================================================
CREATE TABLE IF NOT EXISTS search_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_text TEXT NOT NULL,
    query_embedding VECTOR(1536),
    result_count INT,
    top_score FLOAT,
    execution_time_ms INT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_search_history_created ON search_history(created_at DESC);

-- ============================================================
-- View: source_stats
-- Quick stats view for each source
-- ============================================================
CREATE OR REPLACE VIEW source_stats AS
SELECT
    s.id,
    s.source_type,
    s.title,
    s.url,
    s.status,
    s.created_at,
    COUNT(c.id) as chunk_count,
    COUNT(c.id) FILTER (WHERE c.embedding IS NOT NULL) as embedded_count,
    COALESCE(SUM(c.word_count), 0) as total_words,
    COALESCE(SUM(c.char_count), 0) as total_chars
FROM sources s
LEFT JOIN content_chunks c ON s.id = c.source_id
GROUP BY s.id;

-- ============================================================
-- View: database_stats
-- Overall database statistics
-- ============================================================
CREATE OR REPLACE VIEW database_stats AS
SELECT
    (SELECT COUNT(*) FROM sources) as total_sources,
    (SELECT COUNT(*) FROM sources WHERE status = 'completed') as completed_sources,
    (SELECT COUNT(*) FROM content_chunks) as total_chunks,
    (SELECT COUNT(*) FROM content_chunks WHERE embedding IS NOT NULL) as embedded_chunks,
    (SELECT COALESCE(SUM(word_count), 0) FROM content_chunks) as total_words,
    (SELECT COUNT(DISTINCT source_type) FROM sources) as source_types,
    (SELECT COUNT(*) FROM search_history) as total_searches;

-- ============================================================
-- Function: Update updated_at timestamp
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for sources
DROP TRIGGER IF EXISTS update_sources_updated_at ON sources;
CREATE TRIGGER update_sources_updated_at
    BEFORE UPDATE ON sources
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- Function: Semantic search helper
-- ============================================================
CREATE OR REPLACE FUNCTION search_similar(
    query_embedding VECTOR(1536),
    match_count INT DEFAULT 10,
    match_threshold FLOAT DEFAULT 0.7
)
RETURNS TABLE (
    chunk_id UUID,
    source_id UUID,
    source_type TEXT,
    title TEXT,
    chunk_text TEXT,
    chunk_index INT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id as chunk_id,
        c.source_id,
        s.source_type,
        s.title,
        c.chunk_text,
        c.chunk_index,
        1 - (c.embedding <=> query_embedding) as similarity
    FROM content_chunks c
    JOIN sources s ON c.source_id = s.id
    WHERE c.embedding IS NOT NULL
    AND 1 - (c.embedding <=> query_embedding) >= match_threshold
    ORDER BY c.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- ============================================================
-- Verification
-- ============================================================
DO $$
BEGIN
    RAISE NOTICE 'Schema created successfully';
    RAISE NOTICE 'Tables: sources, content_chunks, search_history';
    RAISE NOTICE 'Views: source_stats, database_stats';
    RAISE NOTICE 'Functions: update_updated_at_column, search_similar';
END $$;
