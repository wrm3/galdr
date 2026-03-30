-- ============================================================
-- Universal RAG Schema for PostgreSQL with pgvector
-- ============================================================
-- Run this in your PostgreSQL database to create the tables
-- Supports: YouTube, Webpages, GitHub, PDFs, Images, Documents
-- ============================================================

-- Enable pgvector extension (should already be enabled)
CREATE EXTENSION IF NOT EXISTS vector;

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

    -- Embedding
    embedding VECTOR(1536),             -- OpenAI text-embedding-3-small

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

-- HNSW index for semantic search (IMPORTANT: use HNSW, not IVFFlat)
CREATE INDEX IF NOT EXISTS idx_content_chunks_embedding ON content_chunks
USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_content_chunks_source ON content_chunks(source_id);
CREATE INDEX IF NOT EXISTS idx_content_chunks_type ON content_chunks(chunk_type);

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
    SUM(c.word_count) as total_words
FROM sources s
LEFT JOIN content_chunks c ON s.id = c.source_id
GROUP BY s.id;

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
-- Grant permissions (adjust as needed)
-- ============================================================
-- GRANT ALL ON sources TO authenticated;
-- GRANT ALL ON content_chunks TO authenticated;
-- GRANT SELECT ON source_stats TO authenticated;
