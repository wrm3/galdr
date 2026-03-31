-- ============================================================
-- 14_content_monitors.sql
-- Scheduled content monitoring — playlists, docs, repos, URLs
-- ============================================================
-- Run order: 14 (after vault_notes)
-- Purpose: Track URLs/playlists/repos on configurable schedules,
--          detect changes, and trigger re-ingestion.
-- ============================================================

CREATE TABLE IF NOT EXISTS content_monitors (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255) UNIQUE NOT NULL,
    monitor_type    VARCHAR(50) NOT NULL
                    CHECK (monitor_type IN ('playlist', 'docs', 'github_repo', 'url')),
    url             TEXT NOT NULL,
    schedule        VARCHAR(50) NOT NULL DEFAULT 'daily'
                    CHECK (schedule IN ('hourly', 'daily', 'weekly', 'monthly')),
    enabled         BOOLEAN NOT NULL DEFAULT true,
    last_checked_at TIMESTAMPTZ,
    last_change_at  TIMESTAMPTZ,
    check_state     JSONB DEFAULT '{}',
    config          JSONB DEFAULT '{}',
    created_by      TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_content_monitors_enabled
    ON content_monitors (enabled, schedule);

CREATE INDEX IF NOT EXISTS idx_content_monitors_due
    ON content_monitors (enabled, last_checked_at)
    WHERE enabled = true;
