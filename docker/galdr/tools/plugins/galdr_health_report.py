"""
galdr_health_report Plugin

Compute a health score for a galdr-managed project by reading its .galdr/ directory.
Returns per-subsystem breakdowns, stale claim detection, and a blocked-task list.

Designed to work with both galdr v1 (template/) and galdr vNext (templates/).
"""
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ============================================================
# PLUGIN METADATA (Required)
# ============================================================

TOOL_NAME = "galdr_health_report"

TOOL_DESCRIPTION = (
    "Compute the health score for a galdr-managed project. "
    "Reads the project's .galdr/TASKS.md and .galdr/tasks/ directory to produce "
    "an overall health score (0-100), per-subsystem breakdown, stale claim detection, "
    "and a list of blocked tasks. "
    "Works for both galdr v1 and galdr vNext (templates) projects."
)

TOOL_PARAMS = {
    "target_path": (
        "Absolute path to the project directory to report on (required). "
        "Must contain a .galdr/ subdirectory with TASKS.md."
    ),
    "claim_ttl_minutes": (
        "Override the default claim TTL for stale detection (default: 120). "
        "Claims older than this many minutes are flagged as stale."
    ),
}

_config = None


def setup(context: dict):
    """Called once at plugin load time."""
    global _config
    _config = context.get("config", {})


# ============================================================
# STATUS INDICATOR MAPPING
# ============================================================

# Map TASKS.md checkbox text to canonical status names
STATUS_PATTERNS = {
    r"\[✅\]": "completed",
    r"\[🔄\]": "in_progress",
    r"\[📋\]": "ready",
    r"\[📝\]": "speccing",
    r"\[🔍\]": "awaiting_verification",
    r"\[❌\]": "failed",
    r"\[⏸️\]": "paused",
    r"\[🌾\]": "harvested",
    r"\[⏳\]": "waiting",
    r"\[ \]": "pending",
}

# Statuses counted as "done" for health score numerator
DONE_STATUSES = {"completed"}

# Statuses excluded from the health denominator (cancelled/harvested/paused)
EXCLUDED_STATUSES = {"failed", "paused", "harvested"}


def _parse_tasks_md(tasks_md_path: Path) -> Dict[str, Any]:
    """
    Parse TASKS.md and return task counts by status, per-subsystem breakdown,
    and raw task list.

    Returns:
        {
            "counts": {"completed": 5, "in_progress": 1, ...},
            "subsystems": [{"name": "...", "counts": {...}}],
            "total": 10,
        }
    """
    if not tasks_md_path.exists():
        return None

    text = tasks_md_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    global_counts: Dict[str, int] = {k: 0 for k in STATUS_PATTERNS.values()}
    global_counts.setdefault("unknown", 0)

    subsystems: List[Dict[str, Any]] = []
    current_subsystem: Optional[str] = None
    sub_counts: Dict[str, int] = {}

    # Compiled patterns
    compiled = [(re.compile(pat), status) for pat, status in STATUS_PATTERNS.items()]
    # Phase/subsystem headers  (## Phase N or ### Subsystem: foo)
    phase_header = re.compile(r"^##+ Phase\s+\d+", re.IGNORECASE)
    subsystem_header = re.compile(r"^###+ Subsystem:\s*(.+)", re.IGNORECASE)
    task_line = re.compile(r"^\s*-\s+\[")

    def flush_subsystem():
        nonlocal current_subsystem, sub_counts
        if current_subsystem is not None:
            subsystems.append({"name": current_subsystem, "counts": dict(sub_counts)})
        current_subsystem = None
        sub_counts = {k: 0 for k in STATUS_PATTERNS.values()}
        sub_counts["unknown"] = 0

    for line in lines:
        sub_match = subsystem_header.match(line)
        if sub_match:
            flush_subsystem()
            current_subsystem = sub_match.group(1).strip()
            sub_counts = {k: 0 for k in STATUS_PATTERNS.values()}
            sub_counts["unknown"] = 0
            continue

        if phase_header.match(line):
            # New phase — flush current subsystem if any
            flush_subsystem()
            continue

        if not task_line.match(line):
            continue

        # Determine status from line content
        matched_status = None
        for pattern, status in compiled:
            if pattern.search(line):
                matched_status = status
                break
        if matched_status is None:
            matched_status = "unknown"

        global_counts[matched_status] = global_counts.get(matched_status, 0) + 1
        if current_subsystem is not None:
            sub_counts[matched_status] = sub_counts.get(matched_status, 0) + 1

    flush_subsystem()

    total = sum(global_counts.values())
    return {"counts": global_counts, "subsystems": subsystems, "total": total}


def _compute_health_score(counts: Dict[str, int], total: int) -> int:
    """
    Health score = completed / (total - excluded) * 100.
    Returns 0 if denominator is 0.
    """
    excluded = sum(counts.get(s, 0) for s in EXCLUDED_STATUSES)
    denominator = total - excluded
    if denominator <= 0:
        return 100  # All tasks are excluded/done — nothing failing
    completed = counts.get("completed", 0)
    return round((completed / denominator) * 100)


def _health_status_label(score: int) -> str:
    if score >= 80:
        return "healthy"
    if score >= 50:
        return "degraded"
    return "critical"


def _scan_stale_claims(tasks_dir: Path, ttl_minutes: int) -> List[Dict[str, str]]:
    """
    Scan task files for YAML `claimed_at` + TTL to detect stale claims.
    Returns list of stale task info dicts.
    """
    stale = []
    if not tasks_dir.exists():
        return stale

    now = datetime.now(timezone.utc)
    claimed_at_pat = re.compile(r"claimed_at:\s*['\"]?(.+?)['\"]?\s*$", re.MULTILINE)
    task_id_pat = re.compile(r"\bid:\s*['\"]?(.+?)['\"]?\s*$", re.MULTILINE)
    claimed_by_pat = re.compile(r"claimed_by:\s*['\"]?(.+?)['\"]?\s*$", re.MULTILINE)
    ttl_pat = re.compile(r"claim_ttl_minutes:\s*(\d+)", re.MULTILINE)

    for task_file in tasks_dir.glob("task*.md"):
        try:
            content = task_file.read_text(encoding="utf-8", errors="replace")
            claimed_at_match = claimed_at_pat.search(content)
            if not claimed_at_match:
                continue
            claimed_at_str = claimed_at_match.group(1).strip()
            if claimed_at_str in ("null", "~", ""):
                continue

            # Parse claimed_at timestamp
            try:
                claimed_at = datetime.fromisoformat(claimed_at_str.replace("Z", "+00:00"))
                if claimed_at.tzinfo is None:
                    claimed_at = claimed_at.replace(tzinfo=timezone.utc)
            except ValueError:
                continue

            # Use file-level TTL if present, else default
            ttl_match = ttl_pat.search(content)
            effective_ttl = int(ttl_match.group(1)) if ttl_match else ttl_minutes

            age_minutes = (now - claimed_at).total_seconds() / 60
            if age_minutes > effective_ttl:
                task_id = task_id_pat.search(content)
                claimed_by = claimed_by_pat.search(content)
                stale.append({
                    "file": task_file.name,
                    "task_id": task_id.group(1).strip() if task_id else "?",
                    "claimed_by": claimed_by.group(1).strip() if claimed_by else "?",
                    "claimed_at": claimed_at_str,
                    "age_minutes": round(age_minutes),
                    "ttl_minutes": effective_ttl,
                })
        except Exception as exc:
            logger.debug(f"galdr_health_report: skipping {task_file.name}: {exc}")

    return stale


def _find_blocked_tasks(tasks_dir: Path) -> List[Dict[str, str]]:
    """
    Scan task files for tasks with status=in-progress or pending that have
    unresolved dependencies (dependencies list non-empty and dep task not completed).
    """
    blocked = []
    if not tasks_dir.exists():
        return blocked

    status_pat = re.compile(r"\bstatus:\s*['\"]?(.+?)['\"]?\s*$", re.MULTILINE)
    deps_pat = re.compile(r"\bdependencies:\s*\[([^\]]*)\]", re.MULTILINE)
    task_id_pat = re.compile(r"\bid:\s*['\"]?(.+?)['\"]?\s*$", re.MULTILINE)
    title_pat = re.compile(r"\btitle:\s*['\"](.+?)['\"]", re.MULTILINE)

    # Build completed set
    completed_ids = set()
    all_tasks = {}
    for f in tasks_dir.glob("task*.md"):
        try:
            c = f.read_text(encoding="utf-8", errors="replace")
            tid = task_id_pat.search(c)
            status = status_pat.search(c)
            if tid and status:
                tid_str = tid.group(1).strip()
                all_tasks[tid_str] = {"file": f.name, "status": status.group(1).strip(), "content": c}
                if status.group(1).strip() == "completed":
                    completed_ids.add(tid_str)
        except Exception:
            pass

    for tid_str, task in all_tasks.items():
        if task["status"] not in ("pending", "in-progress", "in_progress"):
            continue
        deps_match = deps_pat.search(task["content"])
        if not deps_match:
            continue
        raw_deps = deps_match.group(1).strip()
        if not raw_deps:
            continue
        deps = [d.strip().strip("'\"") for d in raw_deps.split(",") if d.strip()]
        unmet = [d for d in deps if d not in completed_ids and d != ""]
        if unmet:
            title = title_pat.search(task["content"])
            blocked.append({
                "task_id": tid_str,
                "title": title.group(1) if title else task["file"],
                "unmet_dependencies": unmet,
            })

    return blocked


async def execute(
    target_path: str,
    claim_ttl_minutes: int = 120,
    context: dict = None,
) -> Dict[str, Any]:
    """
    Compute health score for a galdr-managed project.
    """
    try:
        target = Path(target_path).resolve()
    except Exception as e:
        return {"success": False, "error": f"Invalid target_path: {e}"}

    GALDR_dir = target / ".galdr"
    if not GALDR_dir.exists():
        return {
            "success": False,
            "error": f"No .galdr/ directory found at '{target_path}'",
            "hint": "Run galdr_install first to initialise a galdr project.",
        }

    tasks_md = GALDR_dir / "TASKS.md"
    tasks_dir = GALDR_dir / "tasks"

    # ── Parse TASKS.md ─────────────────────────────────────────────────────────
    parsed = _parse_tasks_md(tasks_md)
    if parsed is None:
        return {
            "success": False,
            "error": f"TASKS.md not found at '{tasks_md}'",
            "hint": "The project may not be initialised. Run galdr_install.",
        }

    counts = parsed["counts"]
    total = parsed["total"]
    subsystems_raw = parsed["subsystems"]

    overall_score = _compute_health_score(counts, total)
    status_label = _health_status_label(overall_score)

    # Per-subsystem scores
    subsystem_summary = []
    for ss in subsystems_raw:
        ss_counts = ss["counts"]
        ss_total = sum(ss_counts.values())
        ss_score = _compute_health_score(ss_counts, ss_total)
        subsystem_summary.append({
            "name": ss["name"],
            "health": ss_score,
            "status": _health_status_label(ss_score),
            "counts": {k: v for k, v in ss_counts.items() if v > 0},
        })

    # Stale claims
    stale_claims = _scan_stale_claims(tasks_dir, claim_ttl_minutes)

    # Blocked tasks
    blocked_tasks = _find_blocked_tasks(tasks_dir)

    # Firecrawl crawl status
    crawl_status_warning = None
    crawl_status_info = None
    platforms_dir = target / ".platforms"
    crawl_status_file = platforms_dir / "CRAWL_STATUS.json"
    if crawl_status_file.exists():
        try:
            import json as _json
            cs = _json.loads(crawl_status_file.read_text(encoding="utf-8"))
            crawl_status_info = cs
            last_date_str = cs.get("last_crawl_date") or cs.get("updated_at", "")[:10]
            if last_date_str:
                try:
                    last_date = datetime.strptime(last_date_str[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
                    days_ago = (datetime.now(timezone.utc) - last_date).days
                    if cs.get("status") == "failed":
                        crawl_status_warning = (
                            f"Last platform docs crawl FAILED on {last_date_str}. "
                            "Platform docs knowledge base may be stale."
                        )
                    elif days_ago > 14:
                        crawl_status_warning = (
                            f"Platform docs last crawled {days_ago} days ago ({last_date_str}). "
                            "Docs may be stale — run: python scripts/platform_crawl.py --target all"
                        )
                except ValueError:
                    pass
        except Exception as e:
            logger.warning(f"Could not read CRAWL_STATUS.json: {e}")

    result = {
        "success": True,
        "project": str(target),
        "overall_health": overall_score,
        "status": status_label,
        "task_counts": {
            "completed": counts.get("completed", 0),
            "in_progress": counts.get("in_progress", 0),
            "awaiting_verification": counts.get("awaiting_verification", 0),
            "ready": counts.get("ready", 0),
            "pending": counts.get("pending", 0),
            "failed": counts.get("failed", 0),
            "paused": counts.get("paused", 0),
            "total": total,
        },
        "subsystems": subsystem_summary,
        "stale_claims": stale_claims,
        "stale_claims_count": len(stale_claims),
        "blocked_tasks": blocked_tasks,
        "blocked_tasks_count": len(blocked_tasks),
        "tasks_md_exists": tasks_md.exists(),
        "tasks_dir_exists": tasks_dir.exists(),
    }
    if crawl_status_warning:
        result["crawl_status_warning"] = crawl_status_warning
    if crawl_status_info:
        result["crawl_status"] = crawl_status_info
    return result
