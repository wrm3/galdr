---
name: g-upgrade
description: Full .galdr/ folder audit, structural migration, and version bump. The ONLY skill (besides g-setup) authorized to write galdr_version to .identity. Run when upgrading galdr version or syncing a project to the current spec.
---
# g-upgrade

**Files Owned**: `.galdr/.identity` (version field only), all `.galdr/` structure

**Activate for**: "upgrade galdr", "sync project to current spec", "migrate .galdr", "galdr version bump", "project is out of date with galdr", after receiving a restructuring doc from the galdr repo.

**Authorization rule**: This skill and `g-setup` are the ONLY things that may write `galdr_version` to `.galdr/.identity`. No other skill, agent, hook, or command may touch that field.

---

## When to Use vs Other Skills

| Situation | Use |
|---|---|
| First time ever setting up galdr in a project | `g-setup` |
| Fixing placeholders, sync drift, YAML fields day-to-day | `g-grooming` |
| **Upgrading to a new galdr version OR aligning a project to the current .galdr spec** | **`g-upgrade`** |
| Nightly TTL resets, health score, sprint plan | `g-cleanup` |

---

## Pre-Flight

Before starting, read:
1. `.galdr/.identity` — note current `galdr_version`
2. The target version (from galdr repo `AGENTS.md` or passed by user)
3. Ask if this is **dry-run** (report only, no changes) or **apply** (fix everything)

```
g-upgrade v{current} → v{target}
Mode: DRY-RUN | APPLY
Project: {project_name} ({project_id})
```

---

## Phase 1: Folder Structure Audit

Check that every required folder exists under `.galdr/`. Create missing ones silently.

**Required folders (all galdr versions):**
```
.galdr/
├── tasks/          ← individual task files
├── bugs/           ← individual bug files
├── prds/           ← PRD files
├── subsystems/     ← per-subsystem spec files
└── reports/        ← cleanup and other reports
```

**Report**: list any folders that were missing and created.

---

## Phase 2: Root File Audit

Check each required root file. For missing files, create from canonical template (content below). For existing files, run the per-file health check in Phase 3.

**Required root files:**

| File | If Missing | Health Check |
|---|---|---|
| `TASKS.md` | Create empty template | Phase 3 → Task Sync |
| `BUGS.md` | Create empty template | Phase 3 → Bug Sync |
| `PLAN.md` | Create empty template | Verify has ## Current Focus and ## Deliverable Index |
| `PRDS.md` | Create empty template | Verify has ## PRD Index table |
| `PROJECT.md` | Create empty template | Phase 3 → Goals Check |
| `CONSTRAINTS.md` | Create with header only | Verify has ## Architectural Constraints |
| `SUBSYSTEMS.md` | Create empty template | Phase 3 → Subsystem Sync |
| `IDEA_BOARD.md` | Create empty template | Verify has ## Active Ideas section |
| `.identity` | **STOP — call g-setup** | Phase 3 → Identity Check |

**Empty templates:**

<details>
<summary>TASKS.md template</summary>

```markdown
# TASKS.md — {project_name}

<!-- Status indicators:
[ ]    = pending (no file yet)
[📋]   = pending (file created, ready to start)
[🔄]   = in-progress
[🔍]   = awaiting-verification
[✅]   = completed
[❌]   = failed/cancelled
[⏸️]   = paused
-->

## Tasks

<!-- Add task entries here grouped by subsystem -->
<!-- Example: - [📋] **Task 001**: Title — acceptance summary -->
```
</details>

<details>
<summary>BUGS.md template</summary>

```markdown
# BUGS.md — {project_name}

| Status | ID | Description | Severity | Subsystems |
|---|---|---|---|---|

<!-- Next Bug ID: 001 -->
```
</details>

<details>
<summary>PLAN.md template</summary>

```markdown
# PLAN.md — {project_name} Master Plan

## Current Focus
{Describe current development focus}

## Deliverable Index

| ID | Title | Status | Subsystems | Notes |
|----|-------|--------|------------|-------|

## Build Order

### Active Work

### Completed

## Milestone History
```
</details>

<details>
<summary>PRDS.md template</summary>

```markdown
# PRDS.md — {project_name}

## PRD Index

| ID | Title | Status | Subsystems | Notes |
|----|-------|--------|------------|-------|

<!-- Status: draft | active | completed | cancelled -->
<!-- Next PRD ID: 001 -->
```
</details>

<details>
<summary>IDEA_BOARD.md template</summary>

```markdown
# IDEA_BOARD.md — {project_name}

## Active Ideas

## Promoted Ideas

## Shelved Ideas
```
</details>

---

## Phase 3: Per-File Deep Health Checks

### 3a. .identity Integrity

Read `.galdr/.identity`. Verify all required fields present:

```ini
project_id=     ← UUID format, required
project_name=   ← matches parent folder name (warn if not)
user_id=        ← present (any value OK)
user_name=      ← present (any value OK)
galdr_version=  ← semver format e.g. 1.0.0
vault_location= ← present ({LOCAL} is valid)
```

- Missing `project_id` → **STOP, call g-setup** (never auto-generate mid-upgrade)
- Missing other fields → fill with sensible defaults, note in report
- `project_name` mismatch with folder → warn user, do NOT auto-change

### 3b. TASKS.md ↔ tasks/ Sync

Activate **g-tasks → SYNC CHECK operation**. Collect results. Auto-fix status mismatches. Report phantoms and orphans without auto-fixing (need human decision).

### 3c. BUGS.md ↔ bugs/ Sync

For each row in `BUGS.md`: check if a matching `bugs/bugNNN_*.md` exists.
- In BUGS.md but no file → PHANTOM ⚠️ (report, offer to create stub)
- File exists but not in BUGS.md → ORPHAN ⚠️ (report, offer to add row)

### 3d. PRDS.md ↔ prds/ Sync

For each row in `PRDS.md`: check if matching `prds/prdNNN_*.md` exists.
- Same phantom/orphan pattern as bugs.

### 3e. SUBSYSTEMS.md ↔ subsystems/ Sync

Activate **g-subsystems → SYNC CHECK operation**. Collect results.

### 3f. PROJECT.md Goals Health

```
□ Has a ## Goals section?            → NO: offer to run g-project CREATE/UPDATE
□ Contains {Goal name} placeholder?  → treat as unfilled, flag
□ Has at least G-01?                 → if not, flag for user
□ Has a ## Mission section?          → NO: flag for user
```

### 3g. Task File YAML Schema Migration

For each `.galdr/tasks/taskNNN_*.md`, check for legacy fields:

| Old Field | Action |
|---|---|
| `phase:` present | Remove field (v3 uses subsystem grouping, not phases) |
| Missing `blast_radius` | Add `blast_radius: low` |
| Missing `requires_verification` | Add `requires_verification: false` |
| Missing `ai_safe` | Add `ai_safe: true` |
| `status: in_progress` | Normalize to `status: in-progress` (hyphen not underscore) |

Report count of files migrated.

### 3h. Bug File YAML Schema Check

For each `.galdr/bugs/bugNNN_*.md`, verify required fields: `id, title, severity, status, created_date`. Add missing with defaults.

### 3i. PRD File YAML Schema Check

For each `.galdr/prds/prdNNN_*.md`, verify required fields: `id, title, status, created_date`. Add missing with defaults.

### 3j. Subsystem Spec Completeness

For each `.galdr/subsystems/*.md`, verify required sections:
- `## Responsibility` present?
- `## Activity Log` table present? (create empty if missing)
- YAML frontmatter has `name, status, dependencies, dependents, locations`?

---

## Phase 4: Placeholder Sweep

Scan ALL `.galdr/**/*.md` for unfilled template placeholders:
```
{project_name}  {Project Name}  {PROJECT_NAME}
{Goal name}     {Measurable outcome}  {Target}
{subsystem-name-1}  {subsystem-name-2}
YYYY-MM-DD   (as literal string, not a date)
[Your name here]  [Developer]
```

Auto-fill `{project_name}` from `.identity` `project_name` field.
Collect all others → ask user once at the end (batch, not per-file).

---

## Phase 5: Version Bump

**Only executed if:**
- Mode is APPLY (not dry-run)
- All critical errors resolved (no missing `.identity`, no STOP conditions)
- User confirms

Write new `galdr_version` to `.galdr/.identity`:

```ini
galdr_version=1.x.x
```

Also append to a version log at `.galdr/reports/UPGRADE_LOG.md`:
```markdown
## {date} — v{old} → v{new}
- Folders created: [list]
- Files created: [list]
- Task YAMLs migrated: N
- Bug YAMLs migrated: N
- Placeholders filled: N
- Phantoms/orphans reported: N (see report)
- Applied by: {user_name}
```

---

## Phase 6: Upgrade Report

Print a full summary to console AND write to `.galdr/reports/UPGRADE_REPORT_{date}.md`:

```
╔══════════════════════════════════════════╗
║  GALDR UPGRADE REPORT                    ║
║  {project_name} | v{old} → v{new}        ║
║  {date}                                  ║
╚══════════════════════════════════════════╝

PHASE 1 — Folder Structure
  ✅ tasks/          exists
  ✅ bugs/           exists
  ⚠️  prds/          CREATED (was missing)
  ✅ subsystems/     exists
  ✅ reports/        exists

PHASE 2 — Root Files
  ✅ TASKS.md        exists
  ⚠️  PRDS.md        CREATED (was missing)
  ✅ BUGS.md         exists
  ✅ PLAN.md         exists
  ✅ PROJECT.md      exists
  ✅ CONSTRAINTS.md  exists
  ✅ SUBSYSTEMS.md   exists
  ✅ IDEA_BOARD.md   exists
  ✅ .identity       valid

PHASE 3 — Deep Health Checks
  Tasks:      12 synced | 0 phantoms | 0 orphans
  Bugs:       3 synced  | 1 phantom (BUG-004 — see below)
  PRDs:       2 synced  | 0 orphans
  Subsystems: 4 synced  | 1 stub added (ui-layer)
  PROJECT.md: Goals present | G-01, G-02 defined
  Task YAMLs: 2 migrated (phase field removed, blast_radius added)
  Bug YAMLs:  0 migrated

PHASE 4 — Placeholders
  Auto-filled: 3 instances of {project_name}
  Needs user:  1 unfilled goal target in PROJECT.md

PHASE 5 — Version Bump
  galdr_version: 1.0.0 → 1.1.0 ✅

══════════════════════════════════════════
MANUAL REVIEW NEEDED (N items):
  ⚠️  BUG-004: in BUGS.md but no bugs/bug004_*.md file
  ⚠️  PROJECT.md: G-01 target metric is still a placeholder
══════════════════════════════════════════
```

---

## Dry-Run Mode

When `dry-run` (default for first invocation on an unknown project):
- Run all phases 1-4
- Do NOT create/modify any files
- Do NOT bump version
- Report what WOULD change
- Ask user: "Apply all changes? (yes/no/selective)"
