-- ============================================================
-- 01_extensions.sql
-- Enable required PostgreSQL extensions for galdr
-- ============================================================
-- Run order: 01 (first)
-- Purpose: Enable pgvector for embedding storage
-- ============================================================

-- Enable pgvector extension (provides vector type and operators)
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable UUID generation (for source IDs)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pg_trgm for fuzzy text search (optional but useful)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Verify extensions are installed
DO $$
BEGIN
    RAISE NOTICE 'Extensions enabled successfully';
    RAISE NOTICE '  - vector (pgvector for embeddings)';
    RAISE NOTICE '  - uuid-ossp (UUID generation)';
    RAISE NOTICE '  - pg_trgm (fuzzy text search)';
END $$;
