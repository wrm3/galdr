# @g-harvest-intake — Harvest Intake

Convert an approved reverse-spec `FEATURES.md` into galdr artifacts (goals, PRDs, subsystems, tasks).

## Purpose
`g-harvest-intake` is the **execution layer** of the harvest pipeline. It reads the output of `g-reverse-spec` and translates approved features into galdr's native structures — without overwriting anything that already exists.

## Usage

```
@g-harvest-intake REVIEW {slug}
@g-harvest-intake DRY-RUN {slug} [--mode=approved|all]
@g-harvest-intake APPLY {slug} [--mode=approved|all|category:{cat}]
```

- `{slug}` — the folder name under `research/harvests/`, e.g., `maestro2`, `galdr_forge`

## Operations

### REVIEW
Show what would be created: goals, PRDs, subsystem candidates (MERGE vs NEW vs FLAGGED), and task groupings. Writes nothing.

### DRY-RUN
Full APPLY simulation — no files written. Outputs INTAKE_REPORT.md preview to console.

### APPLY
Creates all galdr artifacts:

1. **Goals** — Extracts project-level goals from `enables:` fields → appends to `PROJECT.md`
2. **Feature** — One Feature file per feature category → `features/prdNNN_{slug}_{category}.md` + FEATURES.md index
3. **Subsystems** — Checks existing SUBSYSTEMS.md; creates new spec or merges into existing
4. **Tasks** — Groups related features (3-8 per task) → `tasks/taskNNN_*.md` + TASKS.md rows
5. **Intake Report** — `research/harvests/{slug}/INTAKE_REPORT.md` with full audit trail

## FEATURES.md Approval Status

Before running APPLY with `--mode=approved`, open the `FEATURES.md` and set feature statuses:

| Status | Meaning |
|--------|---------|
| `[ ]` | Not yet reviewed |
| `[✅]` | Approved for intake |
| `[❌]` | Rejected (skipped) |
| `[⏸]` | Deferred (skip now, review later) |

## Mode Options

| Mode | What gets processed |
|------|-------------------|
| `--mode=approved` | Only `[✅]` features |
| `--mode=all` | All features (ignores status) |
| `--mode=category:{cat}` | Only features in that category |

## Never Overwrites

- Appends to TASKS.md, SUBSYSTEMS.md, FEATURES.md, PROJECT.md
- Never modifies existing task files, PRD files, or subsystem specs
- Safe to run multiple times (duplicate detection via feature_ids)

## Subsystem Merge Detection

Automatically detects when a proposed subsystem overlaps with an existing one:
- **MERGE** (≥70% overlap) — adds features to existing subsystem's spec
- **FLAG** (30-69%) — logs for human review, skips auto-creation
- **NEW** (<30%) — creates full new subsystem spec in `subsystems/`

## Examples

```
# Preview maestro2 harvest (nothing written)
@g-harvest-intake REVIEW maestro2

# Intake all 168 maestro2 features
@g-harvest-intake APPLY maestro2 --mode=all

# Only intake approved galdr_forge features
@g-harvest-intake APPLY galdr_forge --mode=approved

# Just the character system from maestro2
@g-harvest-intake APPLY maestro2 --mode=category:character-system
```

## Input File
`research/harvests/{slug}/FEATURES.md` (produced by `@g-reverse-spec`)

## See Also
- `@g-reverse-spec` — Analyzes a repo and produces `FEATURES.md`
- `@g-task-new` — Create individual tasks manually
- `@g-subsystems` — Manage subsystems registry directly
