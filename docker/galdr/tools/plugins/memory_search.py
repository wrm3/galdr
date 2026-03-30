"""
memory_search — semantic search across all stored agent sessions.
"""
import logging
from typing import Optional

from ._agent_memory_shared import init, embed, embed_str

logger = logging.getLogger(__name__)

TOOL_NAME = "memory_search"
TOOL_DESCRIPTION = (
    "Semantic search across all stored agent sessions and memory captures. "
    "Returns the most relevant past exchanges matching your query. "
    "Searches both passive (file-based) and active (agent-reported) captures."
)
TOOL_PARAMS = {
    "query":      "Natural language search query (e.g., 'how did we set up the database schema')",
    "project_id": "Filter to a specific project UUID (optional — searches all projects if omitted)",
    "platform":   "Filter by platform: 'cursor' | 'claude_code' | 'antigravity' | 'vscode' (optional)",
    "user_id":    "Filter to a specific user (optional — searches all users if omitted)",
    "limit":      "Max results to return (1-20, default: 5)",
}


def setup(context: dict):
    init(context)


def execute(
    query: str,
    project_id: Optional[str] = None,
    platform: Optional[str] = None,
    user_id: Optional[str] = None,
    limit: int = 5,
) -> dict:
    from ._agent_memory_shared import _db
    if not _db:
        return {"success": False, "error": "Database not available"}

    limit = max(1, min(limit, 20))
    vec = embed(query)
    results = []

    if vec:
        es = embed_str(vec)

        # Search agent_turns (passive captures)
        sql = """
            SELECT t.llm_title, t.llm_description,
                   t.user_message, t.agent_response,
                   t.platform, t.capture_tier, t.created_at,
                   s.conversation_id, p.project_id, p.display_name,
                   1 - (t.embedding <=> %s::vector) AS sim
            FROM agent_turns t
            JOIN agent_sessions s ON s.id = t.session_id
            JOIN agent_projects p ON p.id = s.project_id
            WHERE t.embedding IS NOT NULL
        """
        params: list = [es]
        if project_id:
            sql += " AND p.project_id = %s"; params.append(project_id)
        if platform:
            sql += " AND t.platform = %s"; params.append(platform)
        if user_id:
            sql += " AND t.user_id = %s"; params.append(user_id)
        sql += " ORDER BY t.embedding <=> %s::vector LIMIT %s"
        params += [es, limit]

        with _db.get_cursor() as cur:
                cur.execute(sql, params)
                for row in cur.fetchall():
                    results.append({
                        "type": "turn",
                        "title": row["llm_title"],
                        "description": row["llm_description"],
                        "user_preview": (row["user_message"] or "")[:300],
                        "agent_preview": (row["agent_response"] or "")[:300],
                        "platform": row["platform"],
                        "capture_tier": row["capture_tier"],
                        "created_at": str(row["created_at"]),
                        "conversation_id": row["conversation_id"],
                        "project_id": row["project_id"],
                        "project_name": row["display_name"],
                        "similarity": float(row["sim"]),
                    })

        # Search agent_memory_captures (active captures)
        cap_sql = """
            SELECT c.summary, c.key_decisions, c.files_changed, c.created_at,
                   s.conversation_id, s.platform, p.project_id, p.display_name,
                   1 - (c.embedding <=> %s::vector) AS sim
            FROM agent_memory_captures c
            JOIN agent_sessions s ON s.id = c.session_id
            JOIN agent_projects p ON p.id = c.project_id
            WHERE c.embedding IS NOT NULL
        """
        cap_params: list = [es]
        if project_id:
            cap_sql += " AND p.project_id = %s"; cap_params.append(project_id)
        if platform:
            cap_sql += " AND s.platform = %s"; cap_params.append(platform)
        if user_id:
            cap_sql += " AND c.user_id = %s"; cap_params.append(user_id)
        cap_sql += " ORDER BY c.embedding <=> %s::vector LIMIT %s"
        cap_params += [es, limit]

        with _db.get_cursor() as cur:
                cur.execute(cap_sql, cap_params)
                for row in cur.fetchall():
                    results.append({
                        "type": "capture",
                        "title": (row["summary"] or "")[:120],
                        "description": row["summary"],
                        "key_decisions": row["key_decisions"],
                        "files_changed": row["files_changed"],
                        "platform": row["platform"],
                        "capture_tier": "active",
                        "created_at": str(row["created_at"]),
                        "conversation_id": row["conversation_id"],
                        "project_id": row["project_id"],
                        "project_name": row["display_name"],
                        "similarity": float(row["sim"]),
                    })

        results.sort(key=lambda x: x.get("similarity", 0), reverse=True)
        results = results[:limit]

    return {
        "success": True,
        "query": query,
        "results": results,
        "total": len(results),
        "search_type": "semantic" if vec else "unavailable",
    }
