---
name: g-medkit
description: Single .galdr/ health and repair skill. Detects what the project needs — version migration, structural repair, or routine maintenance — and does exactly that. Replaces g-cleanup, g-grooming, and g-upgrade.
---
# g-medkit

**Files Touched**: `.galdr/` (all files and folders)

**Activate for**: `@g-medkit`, nightly maintenance, "fix galdr", "health check", "upgrade galdr", "project is out of sync", "placeholders", broken TASKS.md, missing files, version mismatch.

**Authorization rule**: `g-medkit` and `g-setup` are the ONLY things that may write `galdr_version` to `.galdr/.identity`. No other skill, agent, hook, or command may touch that field.

---

## Mode Detection (Run First — Determines Everything)

Read `.galdr/.identity`. Based on what you find, select a mode:

```
□ .identity missing entirely?
  → STOP. Invoke g-setup. This is not a repair situation, it's a fresh install.

□ galdr_version in .identity doesn't match the current galdr version?
  → MODE: UPGRADE (full structural migration, then continue through all phases)

□ galdr_version matches, but files/folders are missing or corrupted?
  → MODE: REPAIR (structural fixes + per-file health, skip version bump)

□ galdr_version matches, structure is intact, just routine maintenance?
  → MODE: MAINTAIN (TTL resets, health score, backlog — skip structural phases)
```

Report selected mode at the start:
```
🩺 g-medkit — MODE: {UPGRADE | REPAIR | MAINTAIN}
   Project: {project_name} | galdr v{current} → v{target or "current"}
   Dry-run: YES (pass 'apply' to execute changes) | APPLY
```

Default is **dry-run** on UPGRADE and REPAIR. MAINTAIN always applies immediately (it's safe, automated).

---

## Phase 1: Folder Structure (UPGRADE + REPAIR only)

Verify every required `.galdr/` folder exists. Create missing ones silently.

**Required folders:**
```
tasks/        individual task files
bugs/         individual bug files
prds/         PRD files
subsystems/   per-subsystem spec files
reports/      cleanup and upgrade reports
```

Report any folders created.

---

## Phase 2: Root File Audit (UPGRADE + REPAIR only)

Check each required root file. Create from template if missing. For existing files, run Phase 3 health checks.

| File | If Missing | Health Check |
|---|---|---|
| `TASKS.md` | Create empty template | Phase 3 → Task Sync |
| `BUGS.md` | Create empty template | Phase 3 → Bug Sync |
| `PLAN.md` | Create empty template | Has `## Current Focus` and `## Deliverable Index`? |
| `PRDS.md` | Create empty template | Has `## PRD Index` table? |
| `PROJECT.md` | Create empty template | Phase 3 → Goals Check |
| `CONSTRAINTS.md` | Create header-only stub | Has `## Architectural Constraints`? |
| `SUBSYSTEMS.md` | Create empty template | Phase 3 → Subsystem Sync |
| `IDEA_BOARD.md` | Create empty template | Has `## Active Ideas` section? |

**Empty templates:**

```markdown
<!-- TASKS.md -->
# TASKS.md — {project_name}
## Tasks
```

```markdown
<!-- BUGS.md -->
# BUGS.md — {project_name}
| Status | ID | Description | Severity | Subsystems |
|---|---|---|---|---|
<!-- Next Bug ID: 001 -->
```

```markdown
<!-- PLAN.md -->
# PLAN.md — {project_name}
## Current Focus
## Deliverable Index
| ID | Title | Status | Subsystems | Notes |
|----|-------|--------|------------|-------|
## Milestone History
```

```markdown
<!-- PRDS.md -->
# PRDS.md — {project_name}
## PRD Index
| ID | Title | Status | Subsystems | Notes |
|----|-------|--------|------------|-------|
<!-- Next PRD ID: 001 -->
```

```markdown
<!-- IDEA_BOARD.md -->
# IDEA_BOARD.md — {project_name}
## Active Ideas
## Promoted Ideas
## Shelved Ideas
```

---

## Phase 3: Per-File Deep Health (UPGRADE + REPAIR only)

### 3a. .identity Integrity
Verify all fields present and valid:
```ini
project_id=     ← UUID format — STOP if missing, invoke g-setup
project_name=   ← warn if doesn't match parent folder name
user_id=        ← fill with "unknown" if missing
user_name=      ← fill with "unknown" if missing
galdr_version=  ← semver format
vault_location= ← fill with "{LOCAL}" if missing
```

### 3b. TASKS.md ↔ tasks/ Sync
Activate **g-tasks → SYNC CHECK**. Auto-fix status mismatches (file is source of truth). Report phantoms and orphans without auto-fixing.

### 3c. BUGS.md ↔ bugs/ Sync
For each BUGS.md row: check if `bugs/bugNNN_*.md` exists.
- Missing file → PHANTOM ⚠️ (report + offer stub creation)
- Orphan file → ⚠️ (report + offer to add BUGS.md row)

### 3d. PRDS.md ↔ prds/ Sync
Same phantom/orphan pattern as bugs.

### 3e. SUBSYSTEMS.md ↔ subsystems/ Sync
Activate **g-subsystems → SYNC CHECK**. Add stub entries for subsystems referenced in tasks but missing from registry.

### 3f. PROJECT.md Goals Health
```
□ Has ## Goals section?     → NO: offer g-project CREATE
□ Has {placeholder} text?   → flag for user
□ Has at least G-01?        → if not, flag for user
```

### 3g. Task File YAML Schema Migration (UPGRADE only)
For each `.galdr/tasks/taskNNN_*.md`:

| Condition | Action |
|---|---|
| `phase:` field present | Remove (v3 uses subsystem grouping) |
| Missing `blast_radius` | Add `blast_radius: low` |
| Missing `requires_verification` | Add `requires_verification: false` |
| Missing `ai_safe` | Add `ai_safe: true` |
| `status: in_progress` | Normalize to `in-progress` (hyphen) |

### 3h. Bug + PRD YAML Schema Check
Verify required fields present in each `bugs/` and `prds/` file. Add missing with defaults.

### 3i. Subsystem Spec Completeness
For each `subsystems/*.md`:
- Has `## Responsibility`?
- Has `## Activity Log` table? (create empty if missing)
- YAML frontmatter has `name, status, dependencies, dependents, locations`?

---

## Phase 4: Placeholder Sweep (UPGRADE + REPAIR only)

Scan ALL `.galdr/**/*.md` for unfilled template patterns:
```
{project_name}  {Project Name}  {PROJECT_NAME}
{Goal name}     {Measurable outcome}  {Target}
{subsystem-name-1}    {subsystem-name-2}
YYYY-MM-DD      (literal string, not an actual date)
[Your name here]  [Developer]
```

- Auto-fill `{project_name}` from `.identity`
- Batch all remaining unknowns → ask user **once** at the end

---

## Phase 5: Platform Parity Audit (ALL modes)

Compare file lists between `.cursor/rules/`, `.claude/rules/`, `.agent/rules/`:
- Read `PARITY_EXCLUDES.md` (in this skill's folder) first — skip excluded files
- Files missing from one or more targets → report as parity violation

---

## Phase 6: Routine Maintenance (ALL modes)

### TTL Check
For each `in-progress` task: is `now > claim_expires_at`?
- YES → reset to `pending`, clear claim fields, add `failure_history` entry

### Verification Timeout Check
- `[🔍]` for > 8h → reset to `pending`
- `[🔍]` for > 4h → flag in report only

### Health Score
```
base  = (completed / total_non_cancelled) × 100
-5    per stale [🔄]
-3    per [🔍] > 4h
-10   per task with failure_history > 2
-15   per subsystem with no tasks ever
final = max(0, base − penalties)
Healthy: ≥80 | Degraded: 50-79 | Critical: <50
```

### ACTIVE_BACKLOG.md Regeneration
Write `.galdr/ACTIVE_BACKLOG.md`:
- All non-completed/non-cancelled tasks grouped by subsystem
- Recommended sprint order (priority + blockers resolved first)
- Blocked tasks section
- Human-required tasks section (`ai_safe: false`)

### Dependency Graph
Activate **g-dependency-graph** → regenerate `.galdr/DEPENDENCY_GRAPH.md`

### Sprint Planning (galdr_full only — skip silently in slim)
Activate **g-tasks → SPRINT PLAN** → write result to `.galdr/config/SPRINT.md`

---

## Phase 7: Version Bump (UPGRADE mode only, apply confirmed)

Write new `galdr_version` to `.galdr/.identity`.

Append to `.galdr/reports/UPGRADE_LOG.md`:
```markdown
## {date} — v{old} → v{new}
- Folders created: [list or none]
- Files created: [list or none]
- Task YAMLs migrated: N
- Placeholders filled: N
- Phantoms/orphans reported: N
- Applied by: {user_name}
```

---

## Phase 8: Report

Print to console AND write to `.galdr/reports/MEDKIT_REPORT_{date}.md`:

```
╔══════════════════════════════════════════╗
║  🩺 g-medkit REPORT                      ║
║  {project_name} | MODE: {mode}           ║
║  {date}                                  ║
╚══════════════════════════════════════════╝

STRUCTURE
  ✅ tasks/             exists
  ⚠️  prds/             CREATED
  ✅ TASKS.md           exists
  ⚠️  PRDS.md           CREATED

HEALTH CHECKS
  Tasks:      12 synced | 0 phantoms | 0 orphans
  Bugs:       3 synced  | 1 phantom (BUG-004)
  Subsystems: 4 synced  | 1 stub added
  PROJECT.md: Goals present ✅
  Task YAMLs: 2 migrated

PLACEHOLDERS
  Auto-filled: 3 × {project_name}
  Needs user:  1 (G-01 target in PROJECT.md)

MAINTENANCE
  Health score: 87/100 (Healthy)
  TTL resets: 0
  Backlog: regenerated
  Dependency graph: regenerated

VERSION
  galdr_version: 1.0.0 → 1.1.0 ✅

══════════════════════════════════════════
MANUAL REVIEW NEEDED:
  ⚠️  BUG-004: in BUGS.md but no file in bugs/
  ⚠️  PROJECT.md: G-01 target metric is a placeholder
══════════════════════════════════════════
```

---

## Parity Exclusion List
See `PARITY_EXCLUDES.md` in this skill's folder for files intentionally excluded from the parity audit.
