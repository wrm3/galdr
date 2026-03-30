-- ============================================================
-- 11_user_id_columns.sql
-- Add user_id columns to agent_sessions, agent_turns, and
-- agent_memory_captures for per-user memory segregation.
-- ============================================================
-- Run order: 11 (after all existing schema migrations)
-- Purpose: Enable multi-user memory segregation on shared
--          OKE/Kubernetes deployments. Each user's memory is
--          scoped by their user_id from ~/.galdr/user_config.json.
-- Idempotent: Uses IF NOT EXISTS / CREATE OR REPLACE
-- ============================================================

-- ── agent_sessions: add user_id ─────────────────────────────
ALTER TABLE agent_sessions
    ADD COLUMN IF NOT EXISTS user_id TEXT;

CREATE INDEX IF NOT EXISTS idx_sessions_user_id
    ON agent_sessions (user_id)
    WHERE user_id IS NOT NULL;

-- ── agent_turns: add user_id ────────────────────────────────
ALTER TABLE agent_turns
    ADD COLUMN IF NOT EXISTS user_id TEXT;

CREATE INDEX IF NOT EXISTS idx_turns_user_id
    ON agent_turns (user_id)
    WHERE user_id IS NOT NULL;

-- ── agent_memory_captures: add user_id ──────────────────────
ALTER TABLE agent_memory_captures
    ADD COLUMN IF NOT EXISTS user_id TEXT;

CREATE INDEX IF NOT EXISTS idx_captures_user_id
    ON agent_memory_captures (user_id)
    WHERE user_id IS NOT NULL;

-- ── Fix upsert_agent_project to update user_id on conflict ──
CREATE OR REPLACE FUNCTION upsert_agent_project(
    p_project_id    VARCHAR,
    p_user_id       VARCHAR,
    p_machine_id    VARCHAR,
    p_project_path  TEXT,
    p_display_name  VARCHAR
) RETURNS INTEGER AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO agent_projects (project_id, user_id, machine_id, project_path, display_name)
    VALUES (p_project_id, p_user_id, p_machine_id, p_project_path, p_display_name)
    ON CONFLICT (project_id) DO UPDATE
        SET project_path  = EXCLUDED.project_path,
            display_name  = EXCLUDED.display_name,
            user_id       = COALESCE(NULLIF(EXCLUDED.user_id, ''), agent_projects.user_id),
            machine_id    = COALESCE(NULLIF(EXCLUDED.machine_id, ''), agent_projects.machine_id),
            updated_at    = NOW()
    RETURNING id INTO v_id;
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;
