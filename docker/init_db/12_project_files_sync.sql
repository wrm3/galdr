-- ============================================================
-- 12_project_files_sync.sql
-- Server-side storage for .galdr/ and vault files synced
-- from clients via WebSocket.
-- ============================================================
-- Run order: 12 (after user_id columns)
-- Purpose: Enable .galdr/ file sync to server without bind mounts.
--          The web UI reads from this table instead of the filesystem.
-- Design: One project_id = one user (no multi-user conflict resolution).
-- ============================================================

CREATE TABLE IF NOT EXISTS project_files (
    id              SERIAL PRIMARY KEY,
    project_id      TEXT NOT NULL,
    file_path       TEXT NOT NULL,
    content         TEXT,
    content_hash    VARCHAR(64) NOT NULL,
    version         INTEGER NOT NULL DEFAULT 1,
    file_type       VARCHAR(20) NOT NULL DEFAULT 'galdr',
    last_modified_by TEXT,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_project_file UNIQUE (project_id, file_path)
);

CREATE INDEX IF NOT EXISTS idx_project_files_project
    ON project_files (project_id);

CREATE INDEX IF NOT EXISTS idx_project_files_type
    ON project_files (project_id, file_type);

CREATE INDEX IF NOT EXISTS idx_project_files_updated
    ON project_files (project_id, updated_at DESC);

-- ── Crawl targets table (for Task 407) ──────────────────────
CREATE TABLE IF NOT EXISTS crawl_targets (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255) UNIQUE NOT NULL,
    urls            JSONB NOT NULL DEFAULT '[]',
    max_pages       INTEGER NOT NULL DEFAULT 50,
    max_depth       INTEGER NOT NULL DEFAULT 3,
    visibility      VARCHAR(20) NOT NULL DEFAULT 'public'
                    CHECK (visibility IN ('public', 'internal')),
    created_by      TEXT,
    last_crawled_at TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Seed built-in platform targets
INSERT INTO crawl_targets (name, urls, max_pages, max_depth, visibility)
VALUES
    ('cursor', '["https://docs.cursor.com"]'::jsonb, 100, 3, 'public'),
    ('claude', '["https://docs.anthropic.com"]'::jsonb, 100, 3, 'public'),
    ('gemini', '["https://ai.google.dev/gemini-api/docs"]'::jsonb, 100, 3, 'public')
ON CONFLICT (name) DO NOTHING;
