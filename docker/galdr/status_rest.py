"""
status_rest.py — Status aggregation REST endpoints for galdr web UI.

Routes (added to STATUS_ROUTES list, merged into server.py):
  GET  /api/status              — Unified status overview
  GET  /api/status/crawl        — Per-target crawl freshness
  GET  /api/status/heartbeat    — Heartbeat config and recent runs
  GET  /api/status/health       — Health score with task breakdown
  GET  /api/status/system       — System info (MCP, DB, services)
  GET  /api/heartbeat/history   — Paginated run history
  GET  /api/heartbeat/routines  — Routine list from HEARTBEAT.md
  POST /api/heartbeat/trigger   — Trigger a routine (placeholder)
  GET  /api/search/platform-docs — Search crawled platform docs
  GET  /api/search/all          — Unified search across all knowledge
"""
import json
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import yaml

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

logger = logging.getLogger(__name__)

_db = None
_embedding_gen = None
_config: dict = {}

_PROJECT_PATH = os.environ.get("GALDR_PROJECT_PATH", "/projects/galdr")

# Task-line regex from TASKS.md
_STATUS_MAP = {
    "✅": "completed",
    "🔄": "in_progress",
    "📋": "ready",
    "📝": "speccing",
    "🔍": "awaiting_verification",
    "❌": "failed",
    "⏸️": "paused",
    "🌾": "harvested",
    "⏳": "waiting",
    " ": "pending",
}

_PHASE_RE = re.compile(r"^## Phase (\d+):\s*(.+?)(?:\s*\[(.+?)\])?\s*$")
_TASK_RE = re.compile(r"^- \[([^\]]+)\] \*\*Task (\d+)\*\*:\s*(.+)$")

# HEARTBEAT.md routine heading pattern
_ROUTINE_HEADING_RE = re.compile(r"^### (.+)$")
_FIELD_RE = re.compile(r"^\*\*(.+?)\*\*:\s*(.+)$")


def init_status_rest(*, db=None, embedding_generator=None, config=None):
    global _db, _embedding_gen, _config
    _db = db
    _embedding_gen = embedding_generator
    _config = config or {}
    logger.info("status_rest initialized")


def _galdr_path() -> Path:
    return Path(_PROJECT_PATH) / ".galdr"


def _read_file(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


def _parse_yaml_frontmatter(content: str) -> dict:
    if not content or not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end < 0:
        return {}
    try:
        return yaml.safe_load(content[3:end]) or {}
    except Exception:
        return {}


def _parse_tasks_md() -> dict:
    """Parse TASKS.md and return task counts by status."""
    tasks_md = _galdr_path() / "TASKS.md"
    content = _read_file(tasks_md)
    if content is None:
        return {"total": 0, "completed": 0, "in_progress": 0, "pending": 0, "tasks": []}

    tasks = []
    current_phase = None
    for line in content.splitlines():
        pm = _PHASE_RE.match(line)
        if pm:
            current_phase = int(pm.group(1))
            continue
        tm = _TASK_RE.match(line)
        if tm:
            raw_status = tm.group(1)
            status = _STATUS_MAP.get(raw_status.strip(), "unknown")
            tasks.append({
                "id": int(tm.group(2)),
                "title": tm.group(3).strip(),
                "status": status,
                "phase": current_phase,
            })

    counts: dict[str, int] = {}
    for t in tasks:
        counts[t["status"]] = counts.get(t["status"], 0) + 1

    return {
        "total": len(tasks),
        "completed": counts.get("completed", 0),
        "in_progress": counts.get("in_progress", 0),
        "pending": counts.get("pending", 0) + counts.get("ready", 0),
        "failed": counts.get("failed", 0),
        "awaiting_verification": counts.get("awaiting_verification", 0),
        "counts": counts,
        "tasks": tasks,
    }


def _parse_bugs_md() -> dict:
    bugs_md = _galdr_path() / "BUGS.md"
    content = _read_file(bugs_md)
    if content is None:
        return {"total": 0, "open": 0}

    total = 0
    open_count = 0
    for line in content.splitlines():
        if line.strip().startswith("### BUG-"):
            total += 1
        if re.search(r"\*\*Status\*\*:\s*Open", line, re.IGNORECASE):
            open_count += 1

    return {"total": total, "open": open_count}


def _parse_heartbeat_md() -> dict:
    hb_path = _galdr_path() / "HEARTBEAT.md"
    content = _read_file(hb_path)
    if content is None:
        return {"enabled": False, "config": {}, "routines": []}

    fm = _parse_yaml_frontmatter(content)
    routines = _extract_routines(content)

    return {
        "enabled": fm.get("enabled", False),
        "config": fm,
        "routines": routines,
        "routines_count": len(routines),
    }


def _extract_routines(content: str) -> list[dict]:
    routines = []
    current: Optional[dict] = None

    for line in content.splitlines():
        heading = _ROUTINE_HEADING_RE.match(line)
        if heading:
            if current:
                routines.append(current)
            current = {
                "name": heading.group(1).strip(),
                "schedule": None,
                "agent": None,
                "skill": None,
                "enabled": True,
            }
            continue

        if current is None:
            continue

        field = _FIELD_RE.match(line.strip())
        if field:
            key = field.group(1).strip().lower()
            val = field.group(2).strip().strip("`")
            if key == "schedule":
                current["schedule"] = val
            elif key == "agent":
                current["agent"] = val
            elif key == "skill":
                current["skill"] = val
            elif key == "enabled":
                current["enabled"] = val.lower() in ("true", "yes", "1")

    if current:
        routines.append(current)
    return routines


def _read_budget_tracker() -> dict:
    bt_path = _galdr_path() / "logs" / "heartbeat" / "budget_tracker.json"
    content = _read_file(bt_path)
    if content is None:
        return {"budget_spent": 0, "budget_limit": 5.0}
    try:
        return json.loads(content)
    except Exception:
        return {"budget_spent": 0, "budget_limit": 5.0}


def _detect_alerts(tasks_data: dict, bugs_data: dict) -> list[dict]:
    alerts = []
    for t in tasks_data.get("tasks", []):
        if t["status"] == "in_progress":
            alerts.append({
                "type": "stalled_task",
                "message": f"Task {t['id']} in-progress: {t['title'][:60]}",
            })
    if bugs_data.get("open", 0) > 5:
        alerts.append({
            "type": "high_bug_count",
            "message": f"{bugs_data['open']} open bugs",
        })
    return alerts


def _compute_health_score(tasks_data: dict) -> tuple[int, str]:
    total = tasks_data.get("total", 0)
    if total == 0:
        return 100, "Healthy"
    excluded = tasks_data.get("counts", {}).get("failed", 0) + tasks_data.get("counts", {}).get("paused", 0)
    denom = total - excluded
    if denom <= 0:
        return 100, "Healthy"
    score = round((tasks_data.get("completed", 0) / denom) * 100)
    if score >= 80:
        label = "Healthy"
    elif score >= 50:
        label = "Degraded"
    else:
        label = "Critical"
    return score, label


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

async def handle_status(request: Request) -> JSONResponse:
    """Unified status overview."""
    tasks_data = _parse_tasks_md()
    bugs_data = _parse_bugs_md()
    hb_data = _parse_heartbeat_md()
    budget = _read_budget_tracker()
    health_score, health_label = _compute_health_score(tasks_data)
    alerts = _detect_alerts(tasks_data, bugs_data)

    crawl_targets = []
    if _db:
        try:
            with _db.get_cursor() as cur:
                cur.execute("""
                    SELECT name, last_crawled_at,
                           COALESCE((SELECT r.pages_count FROM platform_docs_crawl_registry r
                            WHERE r.platform = ct.name LIMIT 1), 0) AS pages
                    FROM crawl_targets ct ORDER BY name
                """)
                for row in cur.fetchall():
                    last = row["last_crawled_at"]
                    fresh = False
                    if last:
                        age_days = (datetime.now(timezone.utc) - last.replace(tzinfo=timezone.utc if last.tzinfo is None else last.tzinfo)).days
                        fresh = age_days <= 7
                    crawl_targets.append({
                        "name": row["name"],
                        "fresh": fresh,
                        "last_crawled": str(last) if last else None,
                        "pages": row["pages"],
                    })
        except Exception as e:
            logger.warning("status crawl query failed: %s", e)

    return JSONResponse({
        "health_score": health_score,
        "health_label": health_label,
        "heartbeat": {
            "enabled": hb_data.get("enabled", False),
            "last_run": budget.get("last_run"),
            "budget_spent": budget.get("budget_spent", 0),
            "budget_limit": budget.get("budget_limit", 5.0),
            "routines_count": hb_data.get("routines_count", 0),
        },
        "crawl": {"targets": crawl_targets},
        "tasks": {
            "total": tasks_data["total"],
            "completed": tasks_data["completed"],
            "in_progress": tasks_data["in_progress"],
            "pending": tasks_data["pending"],
        },
        "bugs": bugs_data,
        "alerts": alerts,
    })


async def handle_status_crawl(request: Request) -> JSONResponse:
    """Per-target crawl freshness."""
    if not _db:
        return JSONResponse({"error": "Database not configured"}, status_code=503)

    try:
        with _db.get_cursor() as cur:
            cur.execute("""
                SELECT ct.name, ct.urls, ct.max_pages, ct.max_depth,
                       ct.visibility, ct.last_crawled_at, ct.created_at,
                       COALESCE((SELECT r.pages_count FROM platform_docs_crawl_registry r
                        WHERE r.platform = ct.name LIMIT 1), 0) AS indexed_pages
                FROM crawl_targets ct ORDER BY ct.name
            """)
            targets = []
            for row in cur.fetchall():
                last = row["last_crawled_at"]
                age_days = None
                if last:
                    ldt = last.replace(tzinfo=timezone.utc if last.tzinfo is None else last.tzinfo)
                    age_days = (datetime.now(timezone.utc) - ldt).days
                targets.append({
                    "name": row["name"],
                    "urls": row["urls"],
                    "max_pages": row["max_pages"],
                    "max_depth": row["max_depth"],
                    "visibility": row["visibility"],
                    "last_crawled": str(last) if last else None,
                    "age_days": age_days,
                    "fresh": age_days is not None and age_days <= 7,
                    "indexed_pages": row["indexed_pages"],
                    "created_at": str(row["created_at"]) if row["created_at"] else None,
                })

        return JSONResponse({"targets": targets, "total": len(targets)})

    except Exception as e:
        logger.error("status_crawl error: %s", e)
        return JSONResponse({"error": str(e)}, status_code=500)


async def handle_status_heartbeat(request: Request) -> JSONResponse:
    """Heartbeat config and recent runs."""
    hb_data = _parse_heartbeat_md()
    budget = _read_budget_tracker()

    logs_dir = _galdr_path() / "logs" / "heartbeat"
    recent_runs: list[dict] = []
    if logs_dir.is_dir():
        log_files = sorted(logs_dir.glob("*.md"), key=lambda p: p.name, reverse=True)[:10]
        for lf in log_files:
            content = _read_file(lf)
            fm = _parse_yaml_frontmatter(content) if content else {}
            recent_runs.append({
                "file": lf.name,
                "routine": fm.get("routine", lf.stem),
                "started_at": fm.get("started_at"),
                "status": fm.get("status", "unknown"),
                "cost": fm.get("cost"),
            })

    return JSONResponse({
        "enabled": hb_data.get("enabled", False),
        "config": hb_data.get("config", {}),
        "routines_count": hb_data.get("routines_count", 0),
        "budget": budget,
        "recent_runs": recent_runs,
    })


async def handle_status_health(request: Request) -> JSONResponse:
    """Health score with task breakdown."""
    tasks_data = _parse_tasks_md()
    health_score, health_label = _compute_health_score(tasks_data)

    phase_summary: dict[int, dict] = {}
    for t in tasks_data.get("tasks", []):
        ph = t.get("phase") or 0
        if ph not in phase_summary:
            phase_summary[ph] = {"total": 0, "completed": 0, "in_progress": 0}
        phase_summary[ph]["total"] += 1
        if t["status"] == "completed":
            phase_summary[ph]["completed"] += 1
        elif t["status"] == "in_progress":
            phase_summary[ph]["in_progress"] += 1

    return JSONResponse({
        "health_score": health_score,
        "health_label": health_label,
        "task_counts": {
            "total": tasks_data["total"],
            "completed": tasks_data["completed"],
            "in_progress": tasks_data["in_progress"],
            "pending": tasks_data["pending"],
            "failed": tasks_data.get("failed", 0),
            "awaiting_verification": tasks_data.get("awaiting_verification", 0),
        },
        "counts_by_status": tasks_data.get("counts", {}),
        "phase_summary": {str(k): v for k, v in sorted(phase_summary.items())},
    })


async def handle_status_system(request: Request) -> JSONResponse:
    """System info: MCP server version, loaded plugins, DB status, service URLs."""
    from . import __version__

    db_ok = False
    if _db:
        try:
            with _db.get_cursor() as cur:
                cur.execute("SELECT 1")
            db_ok = True
        except Exception:
            pass

    plugins = []
    try:
        from .plugin_loader import PluginLoader
        plugins_dir = Path(__file__).parent / "tools" / "plugins"
        loader = PluginLoader(plugins_dir)
        plugins = loader.discover_plugins()
    except Exception:
        pass

    return JSONResponse({
        "version": __version__,
        "transport": os.getenv("MCP_TRANSPORT", "stdio"),
        "db_connected": db_ok,
        "embedding_available": _embedding_gen is not None,
        "plugins_loaded": plugins,
        "project_path": _PROJECT_PATH,
        "galdr_dir_exists": _galdr_path().is_dir(),
        "service_urls": {
            "galdr": _config.get("GALDR_url", "http://localhost:8092"),
            "pgadmin": _config.get("pgadmin_url", "http://localhost:8083"),
            "mediawiki": _config.get("mediawiki_url") or "not configured",
        },
    })


async def handle_heartbeat_history(request: Request) -> JSONResponse:
    """Paginated run history from heartbeat and KPI logs."""
    limit = min(max(1, int(request.query_params.get("limit", "20"))), 100)
    offset = max(0, int(request.query_params.get("offset", "0")))

    entries: list[dict] = []

    hb_logs = _galdr_path() / "logs" / "heartbeat"
    if hb_logs.is_dir():
        for lf in sorted(hb_logs.glob("*.md"), key=lambda p: p.name, reverse=True):
            content = _read_file(lf)
            fm = _parse_yaml_frontmatter(content) if content else {}
            entries.append({
                "type": "heartbeat_run",
                "file": lf.name,
                "routine": fm.get("routine", lf.stem),
                "started_at": fm.get("started_at"),
                "status": fm.get("status", "unknown"),
                "cost": fm.get("cost"),
                "duration_s": fm.get("duration_s"),
            })

    kpi_logs = _galdr_path() / "logs" / "kpi"
    if kpi_logs.is_dir():
        for kf in sorted(kpi_logs.glob("*.jsonl"), key=lambda p: p.name, reverse=True):
            try:
                lines = kf.read_text(encoding="utf-8", errors="replace").strip().splitlines()
                for raw_line in lines[-5:]:
                    obj = json.loads(raw_line)
                    entries.append({
                        "type": "kpi",
                        "file": kf.name,
                        "routine": obj.get("routine", kf.stem),
                        "timestamp": obj.get("timestamp"),
                        "metrics": {k: v for k, v in obj.items() if k not in ("routine", "timestamp")},
                    })
            except Exception:
                continue

    entries.sort(key=lambda e: e.get("started_at") or e.get("timestamp") or e.get("file", ""), reverse=True)

    total = len(entries)
    page = entries[offset:offset + limit]

    return JSONResponse({
        "entries": page,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": (offset + limit) < total,
    })


async def handle_heartbeat_routines(request: Request) -> JSONResponse:
    """Parse HEARTBEAT.md routines section."""
    hb_data = _parse_heartbeat_md()
    return JSONResponse({
        "enabled": hb_data.get("enabled", False),
        "routines": hb_data.get("routines", []),
        "total": hb_data.get("routines_count", 0),
    })


async def handle_heartbeat_trigger(request: Request) -> JSONResponse:
    """Trigger a routine (placeholder — actual triggering needs shell access)."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    routine = body.get("routine", "")
    if not routine:
        return JSONResponse({"error": "routine field is required"}, status_code=400)

    hb_data = _parse_heartbeat_md()
    known = [r["name"] for r in hb_data.get("routines", [])]
    if routine not in known:
        return JSONResponse({
            "error": f"Unknown routine: {routine}",
            "known_routines": known,
        }, status_code=404)

    return JSONResponse({
        "success": True,
        "message": f"Routine '{routine}' trigger acknowledged (placeholder — requires host shell access)",
        "routine": routine,
    })


async def handle_search_platform_docs(request: Request) -> JSONResponse:
    """Search platform docs via RAG."""
    if not _db:
        return JSONResponse({"error": "Database not configured"}, status_code=503)

    q = request.query_params.get("q", "")
    if not q:
        return JSONResponse({"error": "q parameter required"}, status_code=400)

    platform = request.query_params.get("platform")
    limit = min(max(1, int(request.query_params.get("limit", "5"))), 25)

    if _embedding_gen:
        try:
            embedding = _embedding_gen.generate(q)
            embed_str = "[" + ",".join(str(x) for x in embedding) + "]"

            sql = """
                SELECT content, metadata,
                       1 - (embedding <=> %s::vector) AS similarity
                FROM memory_captures
                WHERE subject = 'platform_docs'
            """
            params: list = [embed_str]

            if platform:
                sql += " AND metadata->>'platform' = %s"
                params.append(platform.lower())

            sql += " ORDER BY embedding <=> %s::vector LIMIT %s"
            params.extend([embed_str, limit])

            with _db.get_cursor() as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()

            results = []
            for row in rows:
                meta = row.get("metadata") or {}
                if isinstance(meta, str):
                    try:
                        meta = json.loads(meta)
                    except Exception:
                        meta = {}
                results.append({
                    "content": row["content"][:500],
                    "url": meta.get("url", ""),
                    "title": meta.get("title", ""),
                    "platform": meta.get("platform", ""),
                    "score": round(float(row["similarity"]), 4),
                })

            return JSONResponse({"query": q, "mode": "semantic", "results": results, "total": len(results)})

        except Exception as e:
            logger.warning("Semantic search failed, falling back to keyword: %s", e)

    # Keyword fallback
    try:
        with _db.get_cursor() as cur:
            sql = """
                SELECT content, metadata,
                       ts_rank(to_tsvector('english', content),
                               plainto_tsquery('english', %s)) AS rank
                FROM memory_captures
                WHERE subject = 'platform_docs'
                  AND to_tsvector('english', content) @@ plainto_tsquery('english', %s)
            """
            params_kw: list = [q, q]
            if platform:
                sql += " AND metadata->>'platform' = %s"
                params_kw.append(platform.lower())
            sql += " ORDER BY rank DESC LIMIT %s"
            params_kw.append(limit)

            cur.execute(sql, params_kw)
            rows = cur.fetchall()

        results = []
        for row in rows:
            meta = row.get("metadata") or {}
            if isinstance(meta, str):
                try:
                    meta = json.loads(meta)
                except Exception:
                    meta = {}
            results.append({
                "content": row["content"][:500],
                "url": meta.get("url", ""),
                "title": meta.get("title", ""),
                "platform": meta.get("platform", ""),
                "score": round(float(row["rank"]), 4),
            })

        return JSONResponse({"query": q, "mode": "keyword", "results": results, "total": len(results)})

    except Exception as e:
        logger.error("platform-docs search error: %s", e)
        return JSONResponse({"error": str(e)}, status_code=500)


async def handle_search_all(request: Request) -> JSONResponse:
    """Unified search across vault_notes + platform_docs + agent_memory."""
    if not _db:
        return JSONResponse({"error": "Database not configured"}, status_code=503)

    q = request.query_params.get("q", "")
    if not q:
        return JSONResponse({"error": "q parameter required"}, status_code=400)

    source_filter = request.query_params.get("source", "all").lower()
    limit = min(max(1, int(request.query_params.get("limit", "10"))), 50)

    use_semantic = _embedding_gen is not None
    embedding = None
    if use_semantic:
        try:
            embedding = _embedding_gen.generate(q)
        except Exception as e:
            logger.warning("Embedding generation failed, falling back to keyword: %s", e)
            use_semantic = False

    all_results: list[dict] = []

    # --- vault_notes ---
    if source_filter in ("all", "vault"):
        try:
            all_results.extend(_search_vault(q, embedding, use_semantic, limit))
        except Exception as e:
            logger.warning("vault search failed: %s", e)

    # --- platform_docs ---
    if source_filter in ("all", "platform_docs"):
        try:
            all_results.extend(_search_platform(q, embedding, use_semantic, limit))
        except Exception as e:
            logger.warning("platform_docs search failed: %s", e)

    # --- agent memory ---
    if source_filter in ("all", "memory"):
        try:
            all_results.extend(_search_memory(q, embedding, use_semantic, limit))
        except Exception as e:
            logger.warning("memory search failed: %s", e)

    all_results.sort(key=lambda r: r.get("score", 0), reverse=True)

    seen: set[str] = set()
    deduped: list[dict] = []
    for r in all_results:
        key = r.get("path") or r.get("title", "")
        if key not in seen:
            seen.add(key)
            deduped.append(r)

    source_counts: dict[str, int] = {}
    for r in deduped:
        src = r.get("source", "unknown")
        source_counts[src] = source_counts.get(src, 0) + 1

    return JSONResponse({
        "query": q,
        "mode": "semantic" if use_semantic else "keyword",
        "source_filter": source_filter,
        "total": len(deduped),
        "source_counts": source_counts,
        "results": deduped[:limit * 2],
    })


# ---------------------------------------------------------------------------
# Search helpers
# ---------------------------------------------------------------------------

def _snippet(text: str, max_len: int = 300) -> str:
    if not text:
        return ""
    text = text.strip()
    if len(text) <= max_len:
        return text
    return text[:max_len].rsplit(" ", 1)[0] + "..."


def _search_vault(q: str, embedding, use_semantic: bool, limit: int) -> list[dict]:
    results: list[dict] = []
    if use_semantic and embedding:
        embed_str = "[" + ",".join(str(x) for x in embedding) + "]"
        with _db.get_cursor() as cur:
            cur.execute("""
                SELECT path, title, note_type, tags, url, body,
                       1 - (embedding <=> %s::vector) AS similarity
                FROM vault_notes
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, [embed_str, embed_str, limit])
            for row in cur.fetchall():
                results.append({
                    "source": "vault",
                    "path": row["path"],
                    "title": row["title"] or row["path"],
                    "type": row["note_type"],
                    "snippet": _snippet(row.get("body", "")),
                    "score": round(float(row["similarity"]), 4),
                })
    else:
        with _db.get_cursor() as cur:
            cur.execute("""
                SELECT path, title, note_type, tags, url, body,
                       ts_rank(to_tsvector('english', coalesce(title,'') || ' ' || coalesce(body,'')),
                               plainto_tsquery('english', %s)) AS rank
                FROM vault_notes
                WHERE to_tsvector('english', coalesce(title,'') || ' ' || coalesce(body,''))
                      @@ plainto_tsquery('english', %s)
                ORDER BY rank DESC LIMIT %s
            """, [q, q, limit])
            for row in cur.fetchall():
                results.append({
                    "source": "vault",
                    "path": row["path"],
                    "title": row["title"] or row["path"],
                    "type": row["note_type"],
                    "snippet": _snippet(row.get("body", "")),
                    "score": round(float(row["rank"]), 4),
                })
    return results


def _search_platform(q: str, embedding, use_semantic: bool, limit: int) -> list[dict]:
    results: list[dict] = []
    if use_semantic and embedding:
        embed_str = "[" + ",".join(str(x) for x in embedding) + "]"
        with _db.get_cursor() as cur:
            cur.execute("""
                SELECT content, metadata,
                       1 - (embedding <=> %s::vector) AS similarity
                FROM memory_captures
                WHERE subject = 'platform_docs' AND embedding IS NOT NULL
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, [embed_str, embed_str, limit])
            for row in cur.fetchall():
                meta = _parse_metadata(row.get("metadata"))
                results.append({
                    "source": "platform_docs",
                    "path": meta.get("url", ""),
                    "title": meta.get("title", "Platform Doc"),
                    "type": "platform_docs",
                    "snippet": _snippet(row["content"]),
                    "score": round(float(row["similarity"]), 4),
                })
    else:
        with _db.get_cursor() as cur:
            cur.execute("""
                SELECT content, metadata,
                       ts_rank(to_tsvector('english', content),
                               plainto_tsquery('english', %s)) AS rank
                FROM memory_captures
                WHERE subject = 'platform_docs'
                  AND to_tsvector('english', content) @@ plainto_tsquery('english', %s)
                ORDER BY rank DESC LIMIT %s
            """, [q, q, limit])
            for row in cur.fetchall():
                meta = _parse_metadata(row.get("metadata"))
                results.append({
                    "source": "platform_docs",
                    "path": meta.get("url", ""),
                    "title": meta.get("title", "Platform Doc"),
                    "type": "platform_docs",
                    "snippet": _snippet(row["content"]),
                    "score": round(float(row["rank"]), 4),
                })
    return results


def _search_memory(q: str, embedding, use_semantic: bool, limit: int) -> list[dict]:
    results: list[dict] = []
    if use_semantic and embedding:
        embed_str = "[" + ",".join(str(x) for x in embedding) + "]"
        with _db.get_cursor() as cur:
            cur.execute("""
                SELECT c.id, c.summary, c.category, c.topic,
                       p.project_id, p.display_name,
                       1 - (c.embedding <=> %s::vector) AS similarity
                FROM agent_memory_captures c
                JOIN agent_projects p ON c.project_id = p.id
                WHERE c.embedding IS NOT NULL
                ORDER BY c.embedding <=> %s::vector
                LIMIT %s
            """, [embed_str, embed_str, limit])
            for row in cur.fetchall():
                title_parts = [p for p in [row.get("category"), row.get("topic")] if p]
                results.append({
                    "source": "memory",
                    "path": f"memory/capture_{row['id']}",
                    "title": " — ".join(title_parts) if title_parts else f"Capture {row['id']}",
                    "type": row.get("category") or "session_capture",
                    "snippet": _snippet(row.get("summary", "")),
                    "score": round(float(row["similarity"]), 4),
                })
    else:
        with _db.get_cursor() as cur:
            cur.execute("""
                SELECT c.id, c.summary, c.category, c.topic,
                       p.project_id, p.display_name,
                       ts_rank(to_tsvector('english', coalesce(c.summary,'')),
                               plainto_tsquery('english', %s)) AS rank
                FROM agent_memory_captures c
                JOIN agent_projects p ON c.project_id = p.id
                WHERE to_tsvector('english', coalesce(c.summary,''))
                      @@ plainto_tsquery('english', %s)
                ORDER BY rank DESC LIMIT %s
            """, [q, q, limit])
            for row in cur.fetchall():
                title_parts = [p for p in [row.get("category"), row.get("topic")] if p]
                results.append({
                    "source": "memory",
                    "path": f"memory/capture_{row['id']}",
                    "title": " — ".join(title_parts) if title_parts else f"Capture {row['id']}",
                    "type": row.get("category") or "session_capture",
                    "snippet": _snippet(row.get("summary", "")),
                    "score": round(float(row["rank"]), 4),
                })
    return results


def _parse_metadata(meta) -> dict:
    if meta is None:
        return {}
    if isinstance(meta, str):
        try:
            return json.loads(meta)
        except Exception:
            return {}
    if isinstance(meta, dict):
        return meta
    return {}


# ---------------------------------------------------------------------------
# Route list — imported by server.py
# ---------------------------------------------------------------------------

STATUS_ROUTES = [
    Route("/api/status",                handle_status,                methods=["GET"]),
    Route("/api/status/crawl",          handle_status_crawl,          methods=["GET"]),
    Route("/api/status/heartbeat",      handle_status_heartbeat,      methods=["GET"]),
    Route("/api/status/health",         handle_status_health,         methods=["GET"]),
    Route("/api/status/system",         handle_status_system,         methods=["GET"]),
    Route("/api/heartbeat/history",     handle_heartbeat_history,     methods=["GET"]),
    Route("/api/heartbeat/routines",    handle_heartbeat_routines,    methods=["GET"]),
    Route("/api/heartbeat/trigger",     handle_heartbeat_trigger,     methods=["POST"]),
    Route("/api/search/platform-docs",  handle_search_platform_docs,  methods=["GET"]),
    Route("/api/search/all",            handle_search_all,            methods=["GET"]),
]
