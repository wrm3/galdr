-- ============================================================
-- 06_agent_memory_metadata.sql
-- Migration: add richer metadata columns to agent_turns
-- Run order: 06 (after 05_agent_memory.sql)
--
-- New columns capture Claude Code JSONL metadata:
--   session_metadata — gitBranch, cwd, version, requestId from session header
--   file_refs        — file paths touched during the turn (from tool use blocks)
--   tool_names       — names of tools invoked (read_file, edit_file, bash, etc.)
-- ============================================================

ALTER TABLE agent_turns
    ADD COLUMN IF NOT EXISTS session_metadata JSONB    DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS file_refs        TEXT[]   DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS tool_names       TEXT[]   DEFAULT '{}';

-- GIN indexes for array containment queries
-- e.g. SELECT * FROM agent_turns WHERE file_refs @> ARRAY['src/app.py']
CREATE INDEX IF NOT EXISTS idx_agent_turns_file_refs
    ON agent_turns USING GIN(file_refs);

CREATE INDEX IF NOT EXISTS idx_agent_turns_tool_names
    ON agent_turns USING GIN(tool_names);

-- GIN index for JSONB metadata queries
-- e.g. SELECT * FROM agent_turns WHERE session_metadata->>'gitBranch' = 'main'
CREATE INDEX IF NOT EXISTS idx_agent_turns_session_metadata
    ON agent_turns USING GIN(session_metadata);

-- Note: FTS index update (to include file_refs) is intentionally deferred.
-- array_to_string in GIN expressions requires careful immutability checks
-- that vary by PostgreSQL version. The existing idx_agent_turns_fts index
-- on llm_title + llm_description remains unchanged; file_refs are
-- searchable via the GIN array index above.
