-- 07_memory_captures_v2.sql
-- Adds structured memory categories, scope, topic, and diff tracking
-- to agent_memory_captures — inspired by letta-code memory architecture.

-- ── Category column ──────────────────────────────────────────────────────────
ALTER TABLE agent_memory_captures
    ADD COLUMN IF NOT EXISTS category TEXT DEFAULT 'general'
        CHECK (category IN ('procedure','preference','context','correction','decision','general'));

-- ── Scope column ─────────────────────────────────────────────────────────────
ALTER TABLE agent_memory_captures
    ADD COLUMN IF NOT EXISTS scope TEXT DEFAULT 'project'
        CHECK (scope IN ('project','user','session','global'));

-- ── Topic tag (short label for grouping related insights) ────────────────────
ALTER TABLE agent_memory_captures
    ADD COLUMN IF NOT EXISTS topic TEXT;

-- ── Diff tracking (git-style: what was there before, what changed) ───────────
ALTER TABLE agent_memory_captures
    ADD COLUMN IF NOT EXISTS prev_content TEXT;   -- previous summary for this topic

ALTER TABLE agent_memory_captures
    ADD COLUMN IF NOT EXISTS diff_text TEXT;      -- human-readable change description

-- ── Indexes ──────────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_captures_category
    ON agent_memory_captures (category);

CREATE INDEX IF NOT EXISTS idx_captures_scope
    ON agent_memory_captures (scope);

CREATE INDEX IF NOT EXISTS idx_captures_topic
    ON agent_memory_captures (topic)
    WHERE topic IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_captures_project_topic
    ON agent_memory_captures (project_id, topic)
    WHERE topic IS NOT NULL;
