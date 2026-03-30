-- ============================================================
-- 04_grants.sql
-- Permission grants for galdr database user
-- ============================================================
-- Run order: 04 (last)
-- Purpose: Grant appropriate permissions to the galdr user
-- ============================================================

-- The POSTGRES_USER from docker-compose is the owner, so they have full access
-- These grants are for completeness and documentation

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO PUBLIC;

-- Grant table permissions
GRANT ALL PRIVILEGES ON TABLE sources TO PUBLIC;
GRANT ALL PRIVILEGES ON TABLE content_chunks TO PUBLIC;
GRANT ALL PRIVILEGES ON TABLE search_history TO PUBLIC;
GRANT ALL PRIVILEGES ON TABLE subjects TO PUBLIC;

-- Grant view permissions
GRANT SELECT ON source_stats TO PUBLIC;
GRANT SELECT ON database_stats TO PUBLIC;

-- Grant sequence permissions (for any auto-increment if used)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO PUBLIC;

-- Grant function execution
GRANT EXECUTE ON FUNCTION update_updated_at_column() TO PUBLIC;
GRANT EXECUTE ON FUNCTION search_similar(VECTOR(1536), INT, FLOAT) TO PUBLIC;
GRANT EXECUTE ON FUNCTION create_subject_database(TEXT, TEXT, TEXT) TO PUBLIC;
GRANT EXECUTE ON FUNCTION set_default_subject(TEXT) TO PUBLIC;
GRANT EXECUTE ON FUNCTION list_subjects() TO PUBLIC;

-- ============================================================
-- Verification
-- ============================================================
DO $$
BEGIN
    RAISE NOTICE '===========================================';
    RAISE NOTICE 'galdr database initialization complete!';
    RAISE NOTICE '===========================================';
    RAISE NOTICE '';
    RAISE NOTICE 'Extensions enabled:';
    RAISE NOTICE '  - pgvector (embedding storage)';
    RAISE NOTICE '  - uuid-ossp (UUID generation)';
    RAISE NOTICE '  - pg_trgm (fuzzy text search)';
    RAISE NOTICE '';
    RAISE NOTICE 'Tables created:';
    RAISE NOTICE '  - sources (content metadata)';
    RAISE NOTICE '  - content_chunks (text chunks with embeddings)';
    RAISE NOTICE '  - search_history (query analytics)';
    RAISE NOTICE '  - subjects (multi-subject registry)';
    RAISE NOTICE '';
    RAISE NOTICE 'Views created:';
    RAISE NOTICE '  - source_stats (per-source statistics)';
    RAISE NOTICE '  - database_stats (overall statistics)';
    RAISE NOTICE '';
    RAISE NOTICE 'Functions created:';
    RAISE NOTICE '  - search_similar() (semantic search)';
    RAISE NOTICE '  - create_subject_database() (multi-subject)';
    RAISE NOTICE '  - set_default_subject() (multi-subject)';
    RAISE NOTICE '  - list_subjects() (multi-subject)';
    RAISE NOTICE '';
    RAISE NOTICE 'Database ready for galdr MCP server!';
END $$;
