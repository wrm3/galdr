---
name: g-grooming
description: Day-to-day .galdr/ health — fix placeholder text, heal TASKS.md sync drift, validate YAML frontmatter, check Goals, and report. For structural migration or version bumps use g-upgrade instead.
---
# g-grooming

**Files Touched**: `.galdr/**/*.md` (reads and patches, never creates new files)

**Activate for**: `@g-grooming`, "fix galdr files", "placeholders", "sync is broken", "groom project". Called by `g-project-manager` in GROOM mode.

**Does NOT**: create missing folders or root files (use `g-upgrade`), bump `galdr_version` (use `g-upgrade`), do first-time setup (use `g-setup`).

---

## Step 1: Detect Mode

```
□ Does .galdr/ exist with 5+ real (non-template) files?
  → YES: run GROOM steps below
  → NO: stop — invoke g-setup first
□ Is user requesting a version migration or structural change?
  → YES: stop — invoke g-upgrade instead
```

---

## Step 2: Template Placeholder Audit

Scan all `.galdr/**/*.md` for unfilled template patterns:

```
{project_name}    {Project Name}    {PROJECT_NAME}
{Goal name}       {Measurable outcome}    {Target}
{subsystem-name-1}    {subsystem-name-2}
YYYY-MM-DD        (literal string, not an actual date)
[Your name here]  [Developer]
[Brief mission from PROJECT.md]
```

- Auto-fill `{project_name}` from `.galdr/.identity` `project_name` field
- Collect all remaining unknowns → ask user **once** at the end (batch, not per-file interrupt)

---

## Step 3: .identity Check

```
□ Does .galdr/.identity exist?
  → NO: STOP — run g-setup (never auto-create .identity mid-groom)
□ Does it have a valid project_id (UUID format)?
  → NO: STOP — run g-setup
□ Missing other fields (project_name, user_id, user_name, galdr_version, vault_location)?
  → Fill with defaults, note in report
```

---

## Step 4: TASKS.md ↔ tasks/ Sync

Activate **g-tasks → SYNC CHECK operation**. Collect results.

- Status mismatches → auto-fix TASKS.md (file is source of truth)
- Phantoms and orphans → report and offer fix options (do not auto-fix)

---

## Step 5: Task File YAML Validation

For each `.galdr/tasks/taskNNN_*.md`:

**Required fields** — add with defaults if missing:
- `id, title, type, status, priority, subsystems, created_date`

**Recommended fields** — add if missing:
- `blast_radius: low`
- `requires_verification: false`
- `ai_safe: true`

**Stale legacy fields** — flag but do NOT auto-remove (use g-upgrade for migrations):
- `phase:` field → flag as legacy

---

## Step 6: PROJECT.md Goals Health

```
□ .galdr/PROJECT.md exists with a ## Goals section?
  → NO: offer to run g-project CREATE/UPDATE PROJECT.MD
□ Contains {Goal name} or {Measurable outcome} placeholder?
  → Treat as unfilled, flag for user
□ Has at least G-01?
  → If not, flag for user
```

---

## Step 7: SUBSYSTEMS.md Staleness

Collect all unique `subsystems:` values across all task files.
Compare to SUBSYSTEMS.md entries.
Missing entries → add stub rows with `status: active` and note in report.

---

## Step 8: Grooming Report

```
═══════════════════════════════════
GALDR GROOMING REPORT — {date}
═══════════════════════════════════
✅ .identity:        valid
✅ TASKS.md ↔ files: 12/12 synced
⚠️  Placeholders:    3 filled, 1 needs user input
⚠️  YAML upgraded:   2 task files (blast_radius added)
✅ SUBSYSTEMS.md:    4 subsystems, all current
✅ PROJECT.md:       Goals present

ACTIONS TAKEN: [list each change made]
MANUAL REVIEW NEEDED: [list items needing user input]
═══════════════════════════════════
```
