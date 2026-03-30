"""
check_crawl_freshness — check if a platform's docs were crawled recently enough.

Used by galdr-platform-parity agent and crawl4ai scripts to avoid
redundant crawls across multiple projects sharing the same MCP database.

Returns: {"fresh": bool, "last_crawled": str|null, "pages": int, "age_days": int|null}
"""
import logging
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

TOOL_NAME = "check_crawl_freshness"
TOOL_DESCRIPTION = (
    "Check if a platform's documentation is fresh enough in the shared crawl registry. "
    "Returns whether a re-crawl is needed. "
    "Platforms: 'cursor' | 'claude_code' | 'gemini'. "
    "If fresh=true, skip crawling — another project already ingested recent docs. "
    "If fresh=false, run: python scripts/platform_crawl.py --target <platform>"
)
TOOL_PARAMS = {
    "platform":     "Platform to check: 'cursor' | 'claude_code' | 'gemini'",
    "max_age_days": "Max acceptable age in days before considered stale (default: 30)",
}

KNOWN_PLATFORMS = {"cursor", "claude_code", "gemini"}

_db = None


def setup(context: dict):
    global _db
    _db = context.get("db")


async def execute(
    platform: str,
    max_age_days: int = 30,
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not available"}

    platform = platform.lower().strip()
    if platform not in KNOWN_PLATFORMS:
        return {
            "success": False,
            "error": f"Unknown platform '{platform}'. Valid: {sorted(KNOWN_PLATFORMS)}",
        }

    max_age_days = max(1, min(max_age_days, 365))

    try:
        with _db.get_cursor() as cur:
            cur.execute(
                """
                SELECT platform, last_crawled_at, pages_count, crawl_status
                FROM platform_docs_crawl_registry
                WHERE platform = %s
                """,
                (platform,),
            )
            row = cur.fetchone()

        if not row:
            # Row missing — registry not initialized for this platform
            return {
                "success": True,
                "platform": platform,
                "fresh": False,
                "last_crawled": None,
                "pages": 0,
                "age_days": None,
                "status": "never",
                "message": f"Platform '{platform}' not found in registry. Run a crawl.",
            }

        last_crawled_at = row["last_crawled_at"]
        pages_count = row["pages_count"] or 0
        crawl_status = row["crawl_status"] or "never"

        if not last_crawled_at or crawl_status == "never":
            return {
                "success": True,
                "platform": platform,
                "fresh": False,
                "last_crawled": None,
                "pages": pages_count,
                "age_days": None,
                "status": crawl_status,
                "message": f"Platform '{platform}' has never been crawled. Run crawler.",
            }

        now = datetime.now(timezone.utc)
        # Ensure last_crawled_at is tz-aware
        if last_crawled_at.tzinfo is None:
            last_crawled_at = last_crawled_at.replace(tzinfo=timezone.utc)

        age_days = (now - last_crawled_at).days
        fresh = age_days <= max_age_days

        return {
            "success": True,
            "platform": platform,
            "fresh": fresh,
            "last_crawled": last_crawled_at.isoformat(),
            "pages": pages_count,
            "age_days": age_days,
            "max_age_days": max_age_days,
            "status": crawl_status,
            "message": (
                f"Fresh — {age_days} days old (threshold: {max_age_days} days). Skip crawl."
                if fresh
                else f"Stale — {age_days} days old (threshold: {max_age_days} days). Re-crawl needed."
            ),
        }

    except Exception as e:
        logger.exception("check_crawl_freshness failed")
        return {"success": False, "error": str(e)}
