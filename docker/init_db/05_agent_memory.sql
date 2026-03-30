-- ============================================================
-- 05_agent_memory.sql
-- Agent Memory System schema for galdr
-- ============================================================
-- Run order: 05 (after core schema, grants)
-- Purpose: Store AI agent conversation history with semantic search
--          Enables cross-IDE, cross-session memory for all galdr projects
-- Platforms: Cursor (passive), Claude Code (passive), Antigravity (active),
--            VS Code + Claude (active)
-- Identity: keyed by project_id (from .galdr/.project_id) + user_id
--           NOT by filesystem path — survives renames and moves
-- ============================================================

-- ============================================================
-- Table: agent_projects
-- One record per project, identified by stable UUID from .galdr/.project_id
-- project_path is informational only — never used as a lookup key
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_projects (
    id           SERIAL PRIMARY KEY,
    project_id   VARCHAR(64) UNIQUE NOT NULL,  -- "proj_a1b2c3d4" from .galdr/.project_id
    user_id      VARCHAR(64),                   -- "usr_e5f6g7h8" from ~/.galdr/user_config.json
    machine_id   VARCHAR(64),                   -- Windows MachineGuid or generated UUID
    project_path TEXT,                          -- last known filesystem path (informational)
    display_name VARCHAR(255),                  -- last known project folder name
    created_at   TIMESTAMPTZ DEFAULT NOW(),
    updated_at   TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- Table: agent_sessions
-- One record per IDE conversation / agent session
-- conversation_id comes from the IDE's hook payload
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_sessions (
    id              SERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) UNIQUE NOT NULL, -- from hook: agent-complete conversationId
    project_id      INTEGER REFERENCES agent_projects(id) ON DELETE CASCADE,
    platform        VARCHAR(50) NOT NULL,  -- 'cursor' | 'claude_code' | 'antigravity' | 'vscode'
    capture_tier    VARCHAR(20) NOT NULL DEFAULT 'passive',  -- 'passive' (file) | 'active' (agent)
    status          VARCHAR(50),           -- from hook payload (e.g. 'success')
    loop_count      INTEGER,               -- number of agent loops (from Cursor hook)
    session_summary TEXT,                  -- LLM-generated rolling session summary
    started_at      TIMESTAMPTZ,
    ended_at        TIMESTAMPTZ DEFAULT NOW(),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- Table: agent_turns
-- One record per user→assistant exchange within a session
-- Core unit of memory: embedded, searchable, deduplicated
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_turns (
    id              SERIAL PRIMARY KEY,
    session_id      INTEGER REFERENCES agent_sessions(id) ON DELETE CASCADE,
    turn_index      INTEGER NOT NULL,               -- 0-based position in session
    content_hash    VARCHAR(64),                    -- MD5(user_message + agent_response)
    user_message    TEXT,                           -- what the developer typed / said
    agent_response  TEXT,                           -- what the agent replied
    llm_title       VARCHAR(255),                   -- LLM-generated 10-15 word title
    llm_description TEXT,                           -- LLM-generated 2-4 sentence summary
    embedding       vector(1536),                   -- text-embedding-3-small of title+description
    platform        VARCHAR(50),                    -- denormalized for per-platform filtering
    capture_tier    VARCHAR(20) DEFAULT 'passive',  -- denormalized from session
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- Table: agent_memory_captures
-- For Tier 2 (active) captures: agent-submitted summaries
-- Used by memory_capture_session() tool (Antigravity, VS Code)
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_memory_captures (
    id              SERIAL PRIMARY KEY,
    session_id      INTEGER REFERENCES agent_sessions(id) ON DELETE CASCADE,
    project_id      INTEGER REFERENCES agent_projects(id) ON DELETE CASCADE,
    summary         TEXT NOT NULL,          -- agent-provided session summary
    key_decisions   TEXT,                   -- architectural decisions documented by agent
    files_changed   TEXT,                   -- comma-separated list of modified files
    embedding       vector(1536),           -- embedding of summary for search
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- Indexes
-- ============================================================

-- agent_turns: primary semantic search index
CREATE INDEX IF NOT EXISTS idx_agent_turns_embedding
    ON agent_turns USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- agent_turns: full-text search fallback (when no embedding available)
CREATE INDEX IF NOT EXISTS idx_agent_turns_fts
    ON agent_turns USING GIN (
        to_tsvector('english',
            COALESCE(llm_title, '') || ' ' || COALESCE(llm_description, ''))
    );

-- agent_turns: lookup by session, dedup by hash
CREATE INDEX IF NOT EXISTS idx_agent_turns_session
    ON agent_turns(session_id);

CREATE INDEX IF NOT EXISTS idx_agent_turns_content_hash
    ON agent_turns(content_hash);

CREATE INDEX IF NOT EXISTS idx_agent_turns_platform
    ON agent_turns(platform);

-- agent_memory_captures: semantic search for active-tier captures
CREATE INDEX IF NOT EXISTS idx_agent_captures_embedding
    ON agent_memory_captures USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_agent_captures_project
    ON agent_memory_captures(project_id);

-- agent_sessions: lookup by project and conversation
CREATE INDEX IF NOT EXISTS idx_agent_sessions_project
    ON agent_sessions(project_id);

CREATE INDEX IF NOT EXISTS idx_agent_sessions_conversation
    ON agent_sessions(conversation_id);

CREATE INDEX IF NOT EXISTS idx_agent_sessions_platform
    ON agent_sessions(platform);

-- agent_projects: primary lookup by project_id UUID
CREATE INDEX IF NOT EXISTS idx_agent_projects_project_id
    ON agent_projects(project_id);

CREATE INDEX IF NOT EXISTS idx_agent_projects_user_id
    ON agent_projects(user_id);

-- ============================================================
-- Helper function: upsert project record
-- Called by memory_ingest_session and memory_capture_session
-- ============================================================
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
            updated_at    = NOW()
    RETURNING id INTO v_id;
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;
