"""
galdr_validate_task — MCP tool
Hard gate for ARCHITECTURE_CONSTRAINTS.md enforcement.

Reads the constraints file from a project and validates a task against active constraints.
Returns structured pass/fail with specific violations listed.

The tool does NOT block execution — it returns results. The calling rule (31_GALDR_autonomous)
decides what to do: WARNINGS → proceed with care, VIOLATIONS → escalate to human.

This preserves unattended operation for safe tasks while enforcing constraints for risky ones.
"""

import re
from pathlib import Path
from typing import Any, Optional

TOOL_NAME = "galdr_validate_task"
TOOL_DESCRIPTION = (
    "Validate a task against the project's ARCHITECTURE_CONSTRAINTS.md before claiming or starting it. "
    "Returns pass/fail with specific violations listed. "
    "Call before any autonomous task claim. "
    "If no constraints file exists, returns valid=true with constraints_checked=0. "
    "WARNINGS = proceed with extra care. VIOLATIONS = escalate to human before proceeding."
)
TOOL_PARAMS = {
    "type": "object",
    "properties": {
        "project_path": {
            "type": "string",
            "description": "Absolute path to the project root (looks for .galdr/docs/ARCHITECTURE_CONSTRAINTS.md).",
        },
        "task_id": {
            "type": "string",
            "description": "Task ID for logging (e.g. '042' or '42-1').",
        },
        "blast_radius": {
            "type": "string",
            "description": "Blast radius of the task: 'low' | 'medium' | 'high'.",
            "enum": ["low", "medium", "high"],
            "default": "medium",
        },
        "subsystems": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of subsystem names this task will touch.",
            "default": [],
        },
        "files_to_modify": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of file paths this task intends to modify (relative to project root).",
            "default": [],
        },
        "ai_safe": {
            "type": "boolean",
            "description": "Whether this task is marked ai_safe in its YAML frontmatter.",
            "default": True,
        },
    },
    "required": ["project_path", "task_id"],
}

# ── Constraint parsing ────────────────────────────────────────────────────────

# Patterns that indicate constraint categories in ARCHITECTURE_CONSTRAINTS.md
# We look for lines with `- [x]` (active) or `- [ ]` (inactive) prefixes.
_ACTIVE_RE = re.compile(r"^\s*-\s*\[x\]\s*(.+)", re.IGNORECASE)
_INACTIVE_RE = re.compile(r"^\s*-\s*\[\s*\]\s*(.+)", re.IGNORECASE)

# Keywords that indicate a constraint blocks high blast-radius work
_HIGH_BLAST_KEYWORDS = [
    "no high blast", "blast_radius: high", "no autonomous high",
    "high blast requires human", "freeze", "locked",
]
# Keywords that indicate a constraint locks a specific subsystem
_LOCK_KEYWORDS = ["locked", "freeze", "do not modify", "read only", "no changes to"]
# Keywords that indicate production-safety constraints
_PROD_SAFETY_KEYWORDS = ["no direct deploy", "no prod", "staging only", "manual approval required"]


def _parse_constraints(constraints_path: Path) -> list[dict[str, Any]]:
    """Parse ARCHITECTURE_CONSTRAINTS.md into a list of active constraint dicts."""
    constraints = []
    current_section = "general"

    for line in constraints_path.read_text(encoding="utf-8").splitlines():
        # Track section headings
        if line.startswith("## "):
            current_section = line[3:].strip().lower()
            continue
        if line.startswith("# "):
            continue

        active_match = _ACTIVE_RE.match(line)
        if active_match:
            text = active_match.group(1).strip()
            text_lower = text.lower()

            constraint = {
                "text": text,
                "section": current_section,
                "active": True,
                "blocks_high_blast": any(k in text_lower for k in _HIGH_BLAST_KEYWORDS),
                "locked_subsystem": None,
                "prod_safety": any(k in text_lower for k in _PROD_SAFETY_KEYWORDS),
            }

            # Try to extract locked subsystem name
            for kw in _LOCK_KEYWORDS:
                if kw in text_lower:
                    # Grab the word(s) after the keyword
                    idx = text_lower.find(kw)
                    remainder = text[idx + len(kw):].strip().strip(":").strip()
                    if remainder:
                        # Take up to first comma or period
                        locked_name = re.split(r"[,.\s]", remainder)[0].lower()
                        constraint["locked_subsystem"] = locked_name
                    break

            constraints.append(constraint)

    return constraints


def _check_task(
    constraints: list[dict],
    blast_radius: str,
    subsystems: list[str],
    files_to_modify: list[str],
    ai_safe: bool,
) -> tuple[list[str], list[str]]:
    """
    Returns (warnings, violations).
    VIOLATIONS require human escalation.
    WARNINGS require extra care but allow unattended execution.
    """
    warnings: list[str] = []
    violations: list[str] = []

    subsystems_lower = [s.lower() for s in subsystems]
    files_lower = [f.lower() for f in files_to_modify]

    for c in constraints:
        text = c["text"]
        text_lower = text.lower()

        # Hard block: constraint explicitly prohibits high blast autonomous work
        if c["blocks_high_blast"] and blast_radius == "high":
            violations.append(
                f"Constraint blocks high blast-radius autonomous work: '{text}'"
            )

        # Hard block: ai_safe=false with a prod-safety constraint
        if c["prod_safety"] and not ai_safe:
            violations.append(
                f"Production-safety constraint requires ai_safe=true or human review: '{text}'"
            )

        # Locked subsystem check
        if c["locked_subsystem"]:
            locked = c["locked_subsystem"]
            if any(locked in ss for ss in subsystems_lower):
                violations.append(
                    f"Subsystem '{locked}' is locked by constraint: '{text}'"
                )
            # Also check file paths for the locked name
            if any(locked in fp for fp in files_lower):
                warnings.append(
                    f"Files may touch locked subsystem '{locked}' (constraint: '{text}')"
                )

        # General high-blast warning even without explicit constraint
        if blast_radius == "high" and not c["blocks_high_blast"]:
            # Just a structural warning — not a constraint violation
            pass

    # Structural warnings (not from constraints, but from task properties)
    if blast_radius == "high" and not ai_safe:
        violations.append(
            "Task has blast_radius=high AND ai_safe=false — human approval required before autonomous execution."
        )
    elif blast_radius == "high" and ai_safe:
        warnings.append(
            "Task has blast_radius=high — verify acceptance criteria are explicit and evidence requirements are set."
        )

    if blast_radius == "medium" and not ai_safe:
        warnings.append(
            "Task has blast_radius=medium and ai_safe=false — proceed with extra verification."
        )

    return warnings, violations


async def execute(
    project_path: str,
    task_id: str,
    blast_radius: str = "medium",
    subsystems: Optional[list[str]] = None,
    files_to_modify: Optional[list[str]] = None,
    ai_safe: bool = True,
) -> dict[str, Any]:

    subsystems = subsystems or []
    files_to_modify = files_to_modify or []

    project = Path(project_path)
    constraints_path = project / ".galdr" / "docs" / "ARCHITECTURE_CONSTRAINTS.md"
    if not constraints_path.exists():
        constraints_path = project / ".galdr" / "ARCHITECTURE_CONSTRAINTS.md"
    if not constraints_path.exists():
        constraints_path = project / "ARCHITECTURE_CONSTRAINTS.md"

    # No constraints file = pass with zero checks
    if not constraints_path.exists():
        return {
            "valid": True,
            "task_id": task_id,
            "warnings": [],
            "violations": [],
            "constraints_checked": 0,
            "note": "No ARCHITECTURE_CONSTRAINTS.md found — proceeding without constraint validation.",
        }

    try:
        constraints = _parse_constraints(constraints_path)
    except Exception as e:
        return {
            "valid": False,
            "task_id": task_id,
            "warnings": [],
            "violations": [f"Could not parse ARCHITECTURE_CONSTRAINTS.md: {e}"],
            "constraints_checked": 0,
        }

    active_constraints = [c for c in constraints if c["active"]]
    warnings, violations = _check_task(
        active_constraints, blast_radius, subsystems, files_to_modify, ai_safe
    )

    return {
        "valid": len(violations) == 0,
        "task_id": task_id,
        "warnings": warnings,
        "violations": violations,
        "constraints_checked": len(active_constraints),
        "action_required": (
            "ESCALATE TO HUMAN — do not proceed autonomously." if violations
            else ("PROCEED WITH EXTRA CARE — review warnings above." if warnings
                  else "PROCEED — no issues found.")
        ),
    }
