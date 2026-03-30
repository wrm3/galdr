-- ============================================================
-- 09_platform_docs_crawl_registry.sql
-- Registry table tracking when each platform's docs were last crawled.
-- Purpose: Prevent multiple projects from redundantly re-crawling the
--          same official docs (Cursor, Claude, Gemini) within a freshness window.
-- Run order: 09 (after existing schema files)
-- ============================================================

CREATE TABLE IF NOT EXISTS platform_docs_crawl_registry (
    id              SERIAL PRIMARY KEY,
    platform        TEXT NOT NULL UNIQUE,       -- 'cursor' | 'claude_code' | 'gemini'
    last_crawled_at TIMESTAMP WITH TIME ZONE,   -- NULL = never crawled
    pages_count     INT DEFAULT 0,              -- Number of pages stored in last crawl
    crawl_status    TEXT DEFAULT 'never',       -- 'never' | 'success' | 'partial' | 'failed'
    notes           TEXT,                       -- Optional human note (e.g., "manual backfill")
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Seed the three known platforms so check_crawl_freshness always finds a row
INSERT INTO platform_docs_crawl_registry (platform, crawl_status)
VALUES
    ('cursor',      'never'),
    ('claude_code', 'never'),
    ('gemini',      'never')
ON CONFLICT (platform) DO NOTHING;

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_crawl_registry_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_crawl_registry_updated_at ON platform_docs_crawl_registry;
CREATE TRIGGER trg_crawl_registry_updated_at
    BEFORE UPDATE ON platform_docs_crawl_registry
    FOR EACH ROW EXECUTE FUNCTION update_crawl_registry_updated_at();

DO $$
BEGIN
    RAISE NOTICE 'platform_docs_crawl_registry created and seeded with cursor, claude_code, gemini';
END $$;
