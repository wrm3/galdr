"""
Dynamic Tool Plugins Package

This directory contains dynamically loaded MCP tool plugins.
Each .py file (except those starting with _) is automatically
loaded at server startup.

Plugin Categories:
- RAG: rag_search, rag_ingest_text, rag_ingest_url, rag_list_sources, rag_stats
- Subjects: rag_list_subjects, rag_create_subject, rag_delete_subject, rag_set_default_subject
- Oracle: oracle_query, oracle_execute, oracle_describe
- Research: research_query, research_summarize, web_fetch (NO DuckDuckGo)
- MediaWiki: mediawiki_get_page, mediawiki_create_page, mediawiki_update_page, mediawiki_search
- Template: template_install, template_check, template_update

See the plugin_loader.py module for loading logic.
"""
