-- ============================================================
-- 13_vault_notes.sql
-- Vault notes table for semantic search over .md knowledge files
-- ============================================================
-- Run order: 13 (after agent memory and project files)
-- Purpose: Store indexed vault notes with pgvector embeddings
-- Used by: vault_sync, vault_search, vault_search_all, vault_list,
--          vault_read, vault_export_sessions, platform_crawl_trigger
-- ============================================================

CREATE TABLE IF NOT EXISTS vault_notes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    path            TEXT NOT NULL UNIQUE,
    project_id      TEXT DEFAULT '',
    project_name    TEXT DEFAULT '',
    title           TEXT DEFAULT '',
    note_date       DATE,
    note_type       TEXT DEFAULT '',
    source          TEXT DEFAULT '',
    tags            TEXT[] DEFAULT '{}',
    aliases         TEXT[] DEFAULT '{}',
    url             TEXT DEFAULT '',
    source_repo     TEXT DEFAULT '',
    source_type     TEXT DEFAULT '',
    content         TEXT DEFAULT '',
    body            TEXT DEFAULT '',
    frontmatter     JSONB DEFAULT '{}',
    links           TEXT[] DEFAULT '{}',
    content_hash    TEXT DEFAULT '',
    embedding       vector(1536),
    exported_at     TIMESTAMP,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_vault_notes_path ON vault_notes(path);
CREATE INDEX IF NOT EXISTS idx_vault_notes_project_id ON vault_notes(project_id);
CREATE INDEX IF NOT EXISTS idx_vault_notes_note_type ON vault_notes(note_type);
CREATE INDEX IF NOT EXISTS idx_vault_notes_tags ON vault_notes USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_vault_notes_updated ON vault_notes(updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_vault_notes_embedding_hnsw
    ON vault_notes USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION vault_notes_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS vault_notes_updated_at ON vault_notes;
CREATE TRIGGER vault_notes_updated_at
    BEFORE UPDATE ON vault_notes
    FOR EACH ROW
    EXECUTE FUNCTION vault_notes_update_timestamp();

DO $$
BEGIN
    RAISE NOTICE 'vault_notes table created with pgvector embedding index';
END $$;
