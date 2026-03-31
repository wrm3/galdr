"""
monitor_check — Trigger a check for one or all due monitors.

Checks for new content based on monitor type:
- playlist: checks for new videos via video_check_new logic
- github_repo: checks latest commit SHA via GitHub API
- docs: re-crawls via platform_crawl_trigger
- url: checks ETag/Last-Modified headers for changes
"""
import json
import logging
from datetime import datetime, timezone
from typing import Optional

TOOL_NAME = "monitor_check"

TOOL_DESCRIPTION = (
    "Trigger a check for a specific monitor or all due monitors. "
    "Detects new content and triggers re-ingestion when changes are found. "
    "Example: monitor_check(name='ai-playlist') or monitor_check() for all due."
)

TOOL_PARAMS = {
    "name": "Name of a specific monitor to check (optional — checks all due if omitted)",
}

_db = None
_embedding_gen = None
_config = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db, _embedding_gen, _config
    _db = context.get("db")
    _embedding_gen = context.get("embedding_generator")
    _config = context.get("config", {})


async def _check_playlist(monitor: dict) -> dict:
    """Check a YouTube playlist for new videos."""
    import httpx

    url = monitor["url"]
    state = monitor.get("check_state") or {}
    known_ids = set(state.get("known_video_ids", []))

    try:
        from galdr_video_analyzer.core.playlist import get_playlist_videos
        result = await get_playlist_videos(playlist_url=url, limit=200, include_metadata=True)

        if not result.get("success"):
            return {"changed": False, "error": result.get("error", "Playlist fetch failed")}

        current_ids = {v["id"] for v in result.get("videos", []) if "id" in v}
        new_ids = current_ids - known_ids

        new_state = {
            "known_video_ids": list(current_ids),
            "total_videos": len(current_ids),
        }

        return {
            "changed": len(new_ids) > 0,
            "new_video_ids": list(new_ids),
            "new_count": len(new_ids),
            "total": len(current_ids),
            "new_state": new_state,
        }
    except ImportError:
        return {"changed": False, "error": "galdr_video_analyzer not available"}
    except Exception as e:
        return {"changed": False, "error": str(e)}


async def _check_github(monitor: dict) -> dict:
    """Check a GitHub repo for new commits."""
    import httpx
    from urllib.parse import urlparse

    url = monitor["url"]
    state = monitor.get("check_state") or {}
    last_sha = state.get("last_sha", "")

    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2:
        return {"changed": False, "error": "Invalid GitHub URL"}

    owner, repo = parts[0], parts[1].replace(".git", "")
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=1"

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(api_url, headers={"Accept": "application/vnd.github.v3+json"})
            if resp.status_code != 200:
                return {"changed": False, "error": f"GitHub API {resp.status_code}"}
            commits = resp.json()
            if not commits:
                return {"changed": False}

            current_sha = commits[0]["sha"]
            changed = current_sha != last_sha

            return {
                "changed": changed,
                "new_state": {"last_sha": current_sha},
                "previous_sha": last_sha,
                "current_sha": current_sha,
            }
    except Exception as e:
        return {"changed": False, "error": str(e)}


async def _check_url(monitor: dict) -> dict:
    """Check a URL for changes via headers."""
    import httpx

    url = monitor["url"]
    state = monitor.get("check_state") or {}
    last_etag = state.get("etag", "")
    last_modified = state.get("last_modified", "")

    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            resp = await client.head(url)
            current_etag = resp.headers.get("etag", "")
            current_modified = resp.headers.get("last-modified", "")

            changed = False
            if current_etag and current_etag != last_etag:
                changed = True
            elif current_modified and current_modified != last_modified:
                changed = True

            return {
                "changed": changed,
                "new_state": {
                    "etag": current_etag,
                    "last_modified": current_modified,
                },
            }
    except Exception as e:
        return {"changed": False, "error": str(e)}


async def _check_docs(monitor: dict) -> dict:
    """Trigger a docs re-crawl."""
    try:
        from galdr.tools.plugins import platform_crawl_trigger

        config = monitor.get("config") or {}
        result = await platform_crawl_trigger.execute(
            target="custom",
            urls=[monitor["url"]],
            max_pages=config.get("max_pages", 50),
            max_depth=config.get("max_depth", 3),
        )

        return {
            "changed": True,
            "crawl_id": result.get("crawl_id"),
            "new_state": {"last_crawl_id": result.get("crawl_id")},
        }
    except Exception as e:
        return {"changed": False, "error": str(e)}


CHECKERS = {
    "playlist": _check_playlist,
    "github_repo": _check_github,
    "url": _check_url,
    "docs": _check_docs,
}


async def _run_check(monitor: dict) -> dict:
    """Run a single monitor check and update state."""
    monitor_type = monitor["monitor_type"]
    checker = CHECKERS.get(monitor_type)
    if not checker:
        return {"success": False, "name": monitor["name"], "error": f"Unknown type: {monitor_type}"}

    result = await checker(monitor)
    now = datetime.now(timezone.utc)

    try:
        with _db.get_connection() as conn:
            with conn.cursor() as cur:
                update_fields = ["last_checked_at = %s"]
                update_params = [now]

                if result.get("new_state"):
                    update_fields.append("check_state = %s::jsonb")
                    update_params.append(json.dumps(result["new_state"]))

                if result.get("changed"):
                    update_fields.append("last_change_at = %s")
                    update_params.append(now)

                update_params.append(monitor["name"])
                cur.execute(
                    f"UPDATE content_monitors SET {', '.join(update_fields)} WHERE name = %s",
                    update_params,
                )
                conn.commit()
    except Exception as e:
        _logger.error("Failed to update monitor state for %s: %s", monitor["name"], e)

    return {
        "success": True,
        "name": monitor["name"],
        "monitor_type": monitor_type,
        "changed": result.get("changed", False),
        "details": result,
    }


async def execute(name: Optional[str] = None) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}

    try:
        with _db.get_cursor() as cur:
            if name:
                cur.execute(
                    "SELECT id, name, monitor_type, url, schedule, check_state, config FROM content_monitors WHERE name = %s",
                    (name.strip().lower(),),
                )
            else:
                cur.execute(
                    """
                    SELECT id, name, monitor_type, url, schedule, check_state, config
                    FROM content_monitors
                    WHERE enabled = true
                      AND (
                        last_checked_at IS NULL
                        OR (schedule = 'hourly'  AND last_checked_at < NOW() - INTERVAL '1 hour')
                        OR (schedule = 'daily'   AND last_checked_at < NOW() - INTERVAL '1 day')
                        OR (schedule = 'weekly'  AND last_checked_at < NOW() - INTERVAL '7 days')
                        OR (schedule = 'monthly' AND last_checked_at < NOW() - INTERVAL '30 days')
                      )
                    ORDER BY last_checked_at ASC NULLS FIRST
                    LIMIT 20
                    """
                )
            rows = cur.fetchall()

        if not rows:
            msg = f"Monitor '{name}' not found" if name else "No monitors due for checking"
            return {"success": True, "message": msg, "checked": 0, "results": []}

        monitors = []
        for row in rows:
            if isinstance(row, dict):
                monitors.append(row)
            else:
                monitors.append({
                    "id": row[0], "name": row[1], "monitor_type": row[2],
                    "url": row[3], "schedule": row[4], "check_state": row[5],
                    "config": row[6],
                })

        results = []
        for m in monitors:
            r = await _run_check(m)
            results.append(r)

        changed_count = sum(1 for r in results if r.get("changed"))
        return {
            "success": True,
            "checked": len(results),
            "changed": changed_count,
            "results": results,
        }
    except Exception as e:
        _logger.error("Monitor check failed: %s", e)
        return {"success": False, "error": str(e)}
