-- ============================================================
-- 03_multi_subject.sql
-- Multi-subject database support for galdr
-- ============================================================
-- Run order: 03 (after schema)
-- Purpose: Enable separate knowledge domains (subjects)
-- Each subject can have its own database for isolation
-- ============================================================

-- ============================================================
-- Table: subjects
-- Registry of available knowledge subjects/domains
-- ============================================================
CREATE TABLE IF NOT EXISTS subjects (
    id TEXT PRIMARY KEY,                 -- e.g., 'work_knowledge', 'ai_coding', 'personal'
    name TEXT NOT NULL,                  -- Display name
    description TEXT,                    -- Subject description
    database_name TEXT NOT NULL,         -- PostgreSQL database name
    is_default BOOLEAN DEFAULT FALSE,    -- Default subject for queries
    is_active BOOLEAN DEFAULT TRUE,      -- Whether subject is active
    metadata JSONB DEFAULT '{}',         -- Additional metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Only one default allowed
CREATE UNIQUE INDEX IF NOT EXISTS idx_subjects_default
ON subjects(is_default) WHERE is_default = TRUE;

-- ============================================================
-- Default subjects
-- ============================================================
INSERT INTO subjects (id, name, description, database_name, is_default)
VALUES
    ('work_knowledge', 'Work Knowledge', 'Work-related documents, processes, and standards', 'rag_work_knowledge', TRUE),
    ('ai_coding', 'AI & Coding', 'Technical documentation, tutorials, AI/ML resources', 'rag_ai_coding', FALSE)
ON CONFLICT (id) DO NOTHING;

-- ============================================================
-- Function: Create subject database
-- Creates a new database with the RAG schema for a subject
-- ============================================================
CREATE OR REPLACE FUNCTION create_subject_database(
    p_subject_id TEXT,
    p_subject_name TEXT,
    p_description TEXT DEFAULT NULL
)
RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
    v_db_name TEXT;
BEGIN
    -- Generate database name
    v_db_name := 'rag_' || lower(regexp_replace(p_subject_id, '[^a-zA-Z0-9_]', '_', 'g'));

    -- Insert subject record
    INSERT INTO subjects (id, name, description, database_name)
    VALUES (p_subject_id, p_subject_name, p_description, v_db_name)
    ON CONFLICT (id) DO UPDATE SET
        name = EXCLUDED.name,
        description = EXCLUDED.description,
        updated_at = NOW();

    -- NOTE: Actual database creation requires superuser privileges
    -- and should be done externally or via a privileged function
    RAISE NOTICE 'Subject registered: % (database: %)', p_subject_id, v_db_name;

    RETURN v_db_name;
END;
$$;

-- ============================================================
-- Function: Set default subject
-- ============================================================
CREATE OR REPLACE FUNCTION set_default_subject(p_subject_id TEXT)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
BEGIN
    -- Clear existing default
    UPDATE subjects SET is_default = FALSE WHERE is_default = TRUE;

    -- Set new default
    UPDATE subjects SET is_default = TRUE WHERE id = p_subject_id;

    RETURN FOUND;
END;
$$;

-- ============================================================
-- Function: List active subjects
-- ============================================================
CREATE OR REPLACE FUNCTION list_subjects()
RETURNS TABLE (
    subject_id TEXT,
    subject_name TEXT,
    description TEXT,
    database_name TEXT,
    is_default BOOLEAN,
    source_count BIGINT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.id,
        s.name,
        s.description,
        s.database_name,
        s.is_default,
        COALESCE((
            SELECT COUNT(*)
            FROM sources src
            -- In multi-db setup, this would query the subject's database
            -- For now, returns 0 as a placeholder
        ), 0)::BIGINT as source_count
    FROM subjects s
    WHERE s.is_active = TRUE
    ORDER BY s.is_default DESC, s.name;
END;
$$;

-- ============================================================
-- Trigger: Update subjects updated_at
-- ============================================================
DROP TRIGGER IF EXISTS update_subjects_updated_at ON subjects;
CREATE TRIGGER update_subjects_updated_at
    BEFORE UPDATE ON subjects
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- Verification
-- ============================================================
DO $$
DECLARE
    v_count INT;
BEGIN
    SELECT COUNT(*) INTO v_count FROM subjects;
    RAISE NOTICE 'Multi-subject setup complete';
    RAISE NOTICE 'Registered subjects: %', v_count;
    RAISE NOTICE 'Default subject: %', (SELECT id FROM subjects WHERE is_default = TRUE);
END $$;
