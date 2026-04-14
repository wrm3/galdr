---
name: g-skl-harvest-intake
version: 1.0.0
description: >
  Convert a reverse-spec FEATURES.md (produced by g-skl-reverse-spec) into galdr
  artifacts: project goals, PRDs, subsystem specs (merge or create), and tasks.
  This is the "Execute" layer in the Discover → Curate → Execute harvest pipeline.
triggers:
  - g-harvest-intake
  - "harvest intake"
  - "apply harvest"
  - "convert features"
  - "intake reverse-spec"
input: research/harvests/{slug}/FEATURES.md
outputs:
  - .galdr/PROJECT.md (goals section appended)
  - .galdr/features/prdNNN_*.md (one per category)
  - .galdr/FEATURES.md (updated index)
  - .galdr/SUBSYSTEMS.md (new or merged rows)
  - .galdr/subsystems/{name}.md (new spec files)
  - .galdr/TASKS.md (new task rows)
  - .galdr/tasks/taskNNN_*.md (one per feature group)
---

# g-skl-harvest-intake

## Purpose

`g-skl-harvest-intake` is the **companion execution skill** to `g-skl-reverse-spec`.

`g-skl-reverse-spec` writes nothing to `.galdr/` — it produces structured `FEATURES.md` reports for human review.

`g-skl-harvest-intake` is the **execution layer**: it reads a `FEATURES.md`, groups features into coherent galdr artifacts, and writes them to the project. It is called after the human has reviewed and approved features (changing their status to `[✅]`).

It can also run in `--mode=all` to intake every feature regardless of approval status — useful when doing a first-pass intake of a freshly-generated report.

---

## Core Rules

1. **Never overwrite** — always append. Existing PRDs, tasks, and subsystems are never modified.
2. **Detect before creating** — check SUBSYSTEMS.md before creating a new subsystem spec. If an existing subsystem is 70%+ overlapping in scope, merge the new features into it.
3. **Group features into tasks** — do NOT create one task per feature. Group related features within a category into a single coherent task (aim for 3-8 features per task).
4. **Extract goals from `enables:`** — the `enables:` array in each feature often contains project-level goal language. Distill these into goal entries.
5. **PRD per category** — create one PRD file per feature category (e.g., one for Character System, one for 3D Pipeline).
6. **Never filter** — if a feature is approved, intake it exactly as specified. Do not decide it's "too similar" to something existing.
7. **Source references** — every task file must include the `source_files:` from the feature's `FEATURES.md` entry.

---

## When to Use

Use `g-skl-harvest-intake` when:

- You have a completed `FEATURES.md` from `g-skl-reverse-spec` and want to generate tasks/PRDs
- A reverse-spec analysis has been reviewed and features have been approved
- You want to do a full intake of ALL features from a harvest (no approval filter)
- You want a dry-run preview of what would be created before committing

---

## Operations

### REVIEW

```
g-harvest-intake REVIEW {slug}
```

Reads `research/harvests/{slug}/FEATURES.md` and outputs a structured summary:

- Feature count by category and approval status (`[ ]`, `[✅]`, `[❌]`)
- Subsystem candidates and whether they exist in SUBSYSTEMS.md already (MERGE vs NEW)
- PRDs that would be created
- Estimated task count (based on grouping algorithm)
- Goals that would be extracted (preview only)

Does NOT write anything.

---

### APPLY

```
g-harvest-intake APPLY {slug} [--mode=approved|all|category:{cat}]
```

Full intake. Creates all galdr artifacts for the selected features.

**Mode options:**
- `--mode=approved` (default) — only features with `status: "[✅]"` 
- `--mode=all` — all features regardless of status (use for fresh reports)
- `--mode=category:CHARACTER_SYSTEM` — only features in a specific category

**Steps (in order):**

#### Step 1 — Read FEATURES.md
- Load `research/harvests/{slug}/FEATURES.md`
- Parse frontmatter YAML: target_name, features[], subsystem_candidates
- Filter features by mode

#### Step 2 — Extract Project Goals
- For each feature, read `enables:` array
- Identify enables entries that describe project-level outcomes (not implementation details)
- Group by theme → propose 1-3 new project goals
- Append to `PROJECT.md` under `## Goals` only if not already present (fuzzy match)

#### Step 3 — Subsystem Detection and Creation
For each `subsystem_candidates` entry in FEATURES.md frontmatter:
1. Read `.galdr/SUBSYSTEMS.md`
2. Check existing subsystems for name, description, and location overlap
3. **If 70%+ overlap** → mark as MERGE (note which existing subsystem to update; add a comment in that subsystem's spec file under `## Absorbed From` section)
4. **If no overlap or <30% overlap** → create NEW subsystem spec at `.galdr/subsystems/{slug}.md`
5. **If 30-70% overlap** → flag for human review (log in intake report, skip creation)

New subsystem spec format:
```markdown
---
name: "{subsystem-name}"
status: planned
description: "{from subsystem_candidates}"
source: "harvest/{slug}"
created_date: YYYY-MM-DD
dependencies: []
dependents: []
locations:
  skills: []
  services: []
  data_stores: []
  files: []
---

# {Subsystem Name}

## Description
{from subsystem_candidates}

## Features Mapped
{list of feature IDs from this subsystem's category}

## Absorbed From
*(none)*

## Activity Log

| Date | Action | Agent | Notes |
|------|--------|-------|-------|
| YYYY-MM-DD | Created | harvest-intake | Source: {slug} |
```

Update SUBSYSTEMS.md registry row for each new subsystem.

#### Step 4 — Create PRDs
Group features by `category` field. For each category with ≥2 approved features:

1. Assign next available Feature ID (read current max from FEATURES.md)
2. Create `features/prd{NNN}_{slug}_{category_slug}.md`
3. Update FEATURES.md index

PRD file format:
```markdown
---
id: prd{NNN}
title: '{Target} — {Category} Integration'
source: harvest/{slug}
category: {category}
status: draft
created_date: YYYY-MM-DD
feature_ids: [F-001, F-002, ...]
---

# PRD: {Target} — {Category} Integration

## Source
Harvested from `{target_name}` via `g-skl-reverse-spec` analysis.
Feature IDs: {comma-separated list}

## Problem Statement
{Synthesized from feature descriptions: what capability this adds}

## Proposed Features
{For each feature in this category:}
### {feature.name}
{feature.description}

**Enables:**
{feature.enables bullet list}

**Source:** `{feature.source_files}`

## Acceptance Criteria
{Generated from enables[] fields across all features in this category}

## Out of Scope
{Features marked [❌] in this category}
```

#### Step 5 — Create Tasks
Group features within each category into task clusters (3-8 features per task). Grouping heuristic:
- Same subsystem → same task
- Common source module → same task  
- Implementation phase (model → API → UI) → sequential tasks

For each task cluster:
1. Assign next sequential task ID
2. Create `tasks/task{NNN}_{slug}_{group_slug}.md`
3. Add row to TASKS.md under appropriate subsystem header

Task file format:
```markdown
---
id: {NNN}
title: '{Descriptive title for the feature group}'
type: feature
status: pending
priority: {high|medium|low based on feature.effort}
prd: prd{NNN}
subsystems: [{subsystem-slug}]
project_context: >
  Harvested from {target_name} — {category}. Features: {IDs}.
dependencies: []
created_date: YYYY-MM-DD
completed_date: ''
source_harvest: {slug}
feature_ids: [{F-001}, {F-002}, ...]
---

# Task: {title}

## Objective
{Synthesized objective from feature descriptions}

## Feature Breakdown

### {Feature Name} (F-NNN)
{feature.description}

**Source:** `{feature.source_files}`

**Enables:**
{feature.enables bullet list}

---
{repeat for each feature in cluster}

## Acceptance Criteria
{Generated from all enables[] in cluster}

## Implementation Notes
{From ANALYSIS.md deep-dive sections for these features}

## Source References
{All source_files from all features in cluster}
```

#### Step 6 — Write Intake Report
Create `research/harvests/{slug}/INTAKE_REPORT.md`:

```markdown
# Harvest Intake Report — {target_name}

**Date**: YYYY-MM-DD  
**Mode**: {approved|all|category:X}  
**Features processed**: N / total

## Created

### Goals Added: N
{list of goal titles}

### PRDs Created: N
{list of prd files}

### Subsystems
- **New**: {list}
- **Merge**: {list with → target subsystem}
- **Flagged for review**: {list}

### Tasks Created: N
{list of task files with feature IDs}

## Skipped
{features with [❌] status and reason}

## Manual Review Required
{subsystems with 30-70% overlap that weren't auto-resolved}
```

---

### DRY-RUN

```
g-harvest-intake DRY-RUN {slug} [--mode=approved|all]
```

Runs the full APPLY logic but writes nothing. Outputs only the INTAKE_REPORT.md preview to stdout. Useful for verifying groupings before committing.

---

## Subsystem Merge Detection

Before creating a new subsystem, run this check against SUBSYSTEMS.md:

```
For each candidate subsystem (from FEATURES.md subsystem_candidates):
  1. Extract key terms from slug + description
  2. For each existing subsystem row in SUBSYSTEMS.md:
     a. Count term overlap
     b. Check if candidate features' source_files overlap with subsystem's locations:
  3. Score:
     - Slug match (exact or root): +40
     - Description term overlap ≥3 terms: +30
     - source_files overlap with subsystem locations: +20 per overlapping path
     - Same category prefix: +10
  4. Score ≥70 → MERGE recommendation
     Score 30-69 → flag for human review
     Score <30 → create new
```

---

## Task Grouping Algorithm

1. Sort features by category
2. Within each category, cluster by:
   - Shared `source_files` prefix (same module → same cluster)
   - Shared subsystem slug
   - Sequential pipeline stages (group all stage 1-3 of a pipeline into one task)
3. Target cluster size: 3-8 features
4. Max cluster size: 10 (split if exceeded)
5. Single-feature categories → standalone task (no grouping)

---

## Large Harvest Handling (>50 features)

For harvests with >50 approved features:
1. Process categories in alphabetical order
2. Create all subsystems first (Step 3), then PRDs (Step 4), then tasks (Step 5)
3. Write TASKS.md entries only after ALL task files are created
4. Write the INTAKE_REPORT.md last
5. Log progress every 10 tasks: `[harvest-intake] Processed 10/50 features...`

---

## Integration with g-skl-reverse-spec

The full harvest pipeline is:

```
g-reverse-spec ANALYZE {path} --depth thorough
    → research/harvests/{slug}/FEATURES.md (features all [ ])

[Human reviews FEATURES.md, sets [✅]/[❌] on features]

g-harvest-intake REVIEW {slug}
    → preview of what would be created

g-harvest-intake APPLY {slug} --mode=approved
    → .galdr/ artifacts created
    → research/harvests/{slug}/INTAKE_REPORT.md
```

Or for first-pass intake without manual approval:

```
g-harvest-intake APPLY {slug} --mode=all
    → all features processed
    → user reviews tasks/PRDs afterwards
```

---

## Examples

```
# Review what would be created from maestro2 harvest
g-harvest-intake REVIEW maestro2

# Dry-run all features
g-harvest-intake DRY-RUN maestro2 --mode=all

# Apply only approved features
g-harvest-intake APPLY maestro2 --mode=approved

# Apply all features from 3D pipeline category only
g-harvest-intake APPLY galdr_forge --mode=category:3d-pipeline

# Full intake of fresh harvest (no approval step)
g-harvest-intake APPLY maestro2 --mode=all
```

---

## See Also
- `g-skl-reverse-spec` — Produces the `FEATURES.md` this skill consumes
- `g-skl-tasks` — Owns TASKS.md and tasks/ individually
- `g-skl-subsystems` — Owns SUBSYSTEMS.md and subsystems/ individually
- `g-skl-plan` — Owns PLAN.md and features/
- `g-skl-project` — Owns PROJECT.md goals
