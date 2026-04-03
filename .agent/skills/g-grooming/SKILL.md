---
name: g-grooming
description: Step-by-step workflow for initializing blank .galdr/ files, fixing template placeholders, healing sync mismatches, and validating completeness. Called by galdr-project-manager agent or directly via @g-grooming.
---
# galdr-grooming

## When to Use
Called by `g-project-manager` in GROOM mode, or directly via `@g-grooming`.
Use when: fixing broken `.galdr/` files, filling placeholders, healing sync, health check.

## Step 1: Detect Mode
```
□ Does .galdr/ exist with 5+ real (non-template) files?
  → YES: proceed with GROOM steps below
  → NO: invoke galdr-project-manager INITIALIZE mode
```

## Step 2: Template Placeholder Audit
Scan all `.galdr/**/*.md` (root, config/, docs/, tracking/) for these patterns (auto-fill or flag for user):
```
{project_name}  {Project Name}  {PROJECT_NAME}
{Goal name}     {Measurable outcome}  {Target}
{Phase Name}    {subsystem-name-1}    {subsystem-name-2}
[Brief mission from PROJECT.md]
[Phase and focus area]
YYYY-MM-DD   (as literal unfilled date)
[Your name here]  [Developer]
```
Fill from `.galdr/PROJECT.md` where possible. Collect unknowns, ask user once at end.

## Step 3: .project_id Check
```
□ Does .galdr/.project_id exist with valid UUID?
  → NO: python -c "import uuid; print(uuid.uuid4())" → write to .galdr/.project_id
  → Note: Required for memory hooks — missing = silent capture failure
```

## Step 4: TASKS.md ↔ Task File Sync
Search paths (in order):
1. `.galdr/tasks/task{id}_*.md` — active tasks
2. `.galdr/phases/phase*/task{id}_*.md` — archived tasks

Status:
- ✅ ACTIVE = found in tasks/
- 📦 ARCHIVED = found in phases/phase*/
- ⚠️ PHANTOM = not found in either (in TASKS.md but no file)
- ⚠️ ORPHAN = file exists but not in TASKS.md

Auto-fix mismatches: file is source of truth — fix TASKS.md.
Phantoms/orphans: report and offer fix.

## Step 5: Phase File Sync
- Every `## Phase N:` header in TASKS.md → check `phases/phaseN_*.md` exists
- Every `phases/phaseN_*.md` → check header in TASKS.md exists
- Missing phase file → create stub with YAML frontmatter

## Step 6: YAML Frontmatter Validation
Required fields: `id, title, status, priority, phase`
vNext fields: `blast_radius, requires_verification, ai_safe`

Missing required → add with sensible defaults
Missing vNext → add: `blast_radius: "low"`, `requires_verification: false`, `ai_safe: true`, `tags: [legacy-upgraded]`

## Step 7: PROJECT.md Goals health
```
□ `.galdr/PROJECT.md` exists with a Goals section? → NO: generate from mission vision + success criteria
□ Contains {Goal name} or {Measurable outcome}? → treat as missing, regenerate
□ Has at least G-01 and G-02? → if not, flag for user
```

## Step 8: SUBSYSTEMS.md Staleness
Collect all unique values from `subsystems:` fields across all task files.
Compare to SUBSYSTEMS.md entries.
Missing entries → add stub rows with `status: active`.

## Step 9: Grooming Report
```
═══════════════════════════════════
GALDR GROOMING REPORT — {date}
═══════════════════════════════════
✅ .project_id: valid UUID present
✅ TASKS.md ↔ files: 12/12 synced
⚠️  Placeholders filled: 3 (PROJECT.md Goals)
⚠️  Legacy YAML upgraded: 2 task files
❌ Phase sync: phase3_*.md missing — created stub
✅ SUBSYSTEMS.md: 4 subsystems, all current

ACTIONS TAKEN: [list each change]
MANUAL REVIEW NEEDED: [list items needing user input]
═══════════════════════════════════
```
