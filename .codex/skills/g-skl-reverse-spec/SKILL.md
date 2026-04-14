---
name: g-skl-reverse-spec
description: Analyze any external repository and produce a structured FEATURES.md harvest report in research/harvests/{slug}/. Agents are reporters — humans are editors. No .galdr/ writes until human approves APPLY.
---
# g-skl-reverse-spec

**Activate for**: "reverse spec", "analyze this repo", "harvest this project", "what features does X have", "extract features from", "what can we adopt from".

**Files Written**: `research/harvests/{slug}/` — never `.galdr/` directly.

**Core Principle**: Agents are **reporters**. Humans are **editors**. Document everything visible. Never filter by "galdr already has this" or "not relevant." The human decides relevance.

---

## Operations

| Operation | Usage |
|-----------|-------|
| `ANALYZE {repo_url}` | Full 5-pass analysis of a repository |
| `RESUME {slug}` | Continue an interrupted analysis from the last completed pass |
| `APPLY {slug}` | Write approved features to `.galdr/features/` staging |
| `APPLY --dry-run {slug}` | Print what APPLY would create without writing |
| `STATUS {slug}` | Show current harvest state and pass completion |

---

## Operation: ANALYZE

```
ANALYZE https://github.com/user/repo
ANALYZE /path/to/local/repo
```

### Setup

1. Derive `{slug}` from URL: `user/repo` → `user__repo` (normalize: lowercase, `/` → `__`, `.` → `-`)
2. Create output dir: `research/harvests/{slug}/`
3. Check for existing harvest: if `FEATURES.md` exists and is < 30 days old → offer RESUME instead
4. Write `_harvest_meta.yaml`:
   ```yaml
   source: {url}
   slug: {slug}
   started: {YYYY-MM-DD}
   passes_completed: []
   ```

### 5-Pass Strategy

Each pass writes its output file before the next pass begins. If context runs out mid-pass, run RESUME.

---

#### Pass 1: Skeleton 📦

**Goal**: Map the top-level architecture — what kind of project is this?

**Read**:
- `README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md` (if any)
- Root directory listing (file/folder names only, no content)
- `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod` (dependencies only)

**Write** → `research/harvests/{slug}/01_skeleton.md`:
```markdown
---
pass: 1
slug: {slug}
source: {url}
completed: {YYYY-MM-DD}
---
# Pass 1: Skeleton

## Project Type
[e.g., Electron app, Python CLI, FastAPI server, React SPA]

## Technology Stack
[Key languages, frameworks, databases from dependency files]

## Root Structure
[Top-level directories and their apparent purpose]

## README Summary
[3-5 bullet summary of what the project does]

## Initial Feature Surface Estimate
[Rough estimate: ~N major feature areas visible from structure]
```

---

#### Pass 2: Module Map 🗂️

**Goal**: Map each top-level module/folder to its responsibilities.

**Read**: One directory listing per top-level folder (no file content yet).

**Write** → `research/harvests/{slug}/02_module_map.md`:
```markdown
---
pass: 2
slug: {slug}
completed: {YYYY-MM-DD}
---
# Pass 2: Module Map

| Module | Path | Responsibility | Interesting? |
|--------|------|----------------|-------------|
| backend/ | src/backend/ | Express API server | ✓ |
| agents/ | src/agents/ | AI orchestration layer | ✓ |
```

---

#### Pass 3: Feature Scan 🔍

**Goal**: Read the most important files in each module and catalog every distinct feature.

**Read**: Key files (entry points, main classes, route definitions, config schemas). For each module flagged "Interesting?" in Pass 2, read 2-5 representative files.

**Reporter Rule**: Document every distinct capability observed. Do NOT skip features because "the target project already has this." The human decides what to adopt.

**Write** → `research/harvests/{slug}/03_feature_scan.md`:
```markdown
---
pass: 3
slug: {slug}
completed: {YYYY-MM-DD}
features_found: N
---
# Pass 3: Feature Scan

## Features Catalog

### [Module Name]

#### F-001: {Feature Name}
- **Description**: What this does in 1-2 sentences
- **Source files**: `path/to/file.ext` (line N)
- **Enables**: [capability this unlocks for users]
- **Effort**: S/M/L/XL
- **Notes**: Any implementation nuance worth preserving

#### F-002: ...
```

---

#### Pass 4: Deep Dives 🔬

**Goal**: For features worth detailed examination, read the full implementation.

**Which features get deep dives**: Any feature with `Effort: M/L/XL` that uses a non-trivial pattern, architecture, or algorithm. User can also explicitly request deep dives.

**For large repos (>200K LOC)**: Ask the user which modules to deep-dive. Don't read everything — context is finite.

**Write** → `research/harvests/{slug}/04_deep_dives.md`:
```markdown
---
pass: 4
slug: {slug}
completed: {YYYY-MM-DD}
features_deep_dived: [F-003, F-007, F-012]
---
# Pass 4: Deep Dives

## F-003: {Feature Name} — Deep Dive

### Architecture
[How it's structured — classes, data flow, key algorithms]

### Key Files
- `path/to/core.ext`: [what it does]

### Adoption Notes
[How this could be adopted — what's transferable vs what's tightly coupled]

### Risks / Dependencies
[External deps, OS-specific code, license concerns]
```

---

#### Pass 5: Synthesis 📋

**Goal**: Produce the final FEATURES.md — the human-readable harvest report.

**Write** → `research/harvests/{slug}/FEATURES.md`:
```markdown
---
target_name: {project name}
source: {url}
slug: {slug}
harvested: {YYYY-MM-DD}
passes_completed: [1, 2, 3, 4, 5]
features_total: N
features_approved: 0
analyst: {agent-id or "human"}
---

# Harvest: {project name}

## Summary
[3-5 sentences about the project and what makes it worth harvesting]

## Feature Catalog

| ID | Feature | Effort | Status | Notes |
|----|---------|--------|--------|-------|
| F-001 | Feature Name | S | [ ] pending | brief note |
| F-002 | Feature Name | M | [ ] pending | |

---

## Feature Details

### F-001: {Feature Name}
**Status**: `[ ] pending` → set to `[✅] approved` to include in APPLY

**Description**: What this does

**Enables**: User-visible capability this unlocks

**Source files**:
- `path/to/file.ext`

**Effort**: S (< 1 day) / M (1-3 days) / L (1 week) / XL (multi-week)

**Adoption approach**: [onboard: port existing patterns] OR [rewrite: build fresh from spec]

**Notes**: Implementation details, gotchas, dependencies

---

### F-002: ...
```

Update `_harvest_meta.yaml`:
```yaml
passes_completed: [1, 2, 3, 4, 5]
completed: {YYYY-MM-DD}
features_total: N
status: ready_for_review
```

---

## Operation: RESUME

```
RESUME user__repo
```

1. Read `research/harvests/{slug}/_harvest_meta.yaml` → `passes_completed`
2. Find highest completed pass → continue from pass N+1
3. If `passes_completed: [1,2,3,4,5]` → "Harvest complete. Run APPLY to create feature staging docs."

---

## Operation: APPLY

```
APPLY user__repo
APPLY --dry-run user__repo
```

Reads `research/harvests/{slug}/FEATURES.md` and creates `.galdr/features/` staging documents for each `[✅] approved` feature.

### What APPLY creates

For each `[✅] approved` feature:
1. **Check for an existing related staging feature** in `.galdr/features/` — if found, add a "Collected Approaches" entry (via `g-skl-features COLLECT`) instead of creating a duplicate
2. **Create new staging feature** at `.galdr/features/featNNN_{slug}_{feature_slug}.md`:
   ```yaml
   ---
   id: feat-NNN
   title: '{Feature Name} (from {source_name})'
   status: staging
   goal: ''
   min_tier: slim
   subsystems: []
   harvest_sources: ['{source_url}']
   created_date: '{YYYY-MM-DD}'
   promoted_date: ''
   committed_date: ''
   completed_date: ''
   ---

   # Feature: {title}

   ## Summary
   {description from FEATURES.md}

   ## Collected Approaches

   ### From {source_name} ({source_url})
   {adoption notes from FEATURES.md}

   **Source files**: `path/to/file.ext`

   ## Potential Deliverables
   {generated from feature description}

   ## Draft Tasks
   <!-- Populate when promoting to specced -->
   ```

3. **Add to `FEATURES.md` index** under Staging section
4. **Update `_harvest_meta.yaml`**: `features_approved: N`, `applied: YYYY-MM-DD`

### --dry-run mode

Print to stdout without writing:
```
DRY RUN — APPLY user__repo
Would create:
  .galdr/features/feat-036_user__repo_feature_name.md
  .galdr/features/feat-037_user__repo_another_feature.md
Update .galdr/FEATURES.md: +2 staging entries
Run without --dry-run to apply.
```

### Apply modes (per feature)

Set in FEATURES.md feature frontmatter:
- `onboard`: Port the existing patterns and idioms from the source
- `rewrite`: Use the spec as design input, build fresh from galdr conventions

---

## Operation: STATUS

```
STATUS user__repo
```

Prints:
```
Harvest: user__repo (github.com/user/repo)
Passes: [1✅, 2✅, 3✅, 4⬜, 5⬜]
Features found: 23 (Pass 3)
Last updated: 2026-04-10
Status: Pass 4 pending — run ANALYZE to continue
```

---

## Output Directory Layout

```
research/harvests/{slug}/
├── _harvest_meta.yaml      # state tracking
├── 01_skeleton.md          # Pass 1 output
├── 02_module_map.md        # Pass 2 output
├── 03_feature_scan.md      # Pass 3 output
├── 04_deep_dives.md        # Pass 4 output (if needed)
└── FEATURES.md             # Pass 5 synthesis (review target)
```

---

## Feature Status Codes

In `FEATURES.md`:
| Code | Meaning |
|------|---------|
| `[ ] pending` | Not yet reviewed |
| `[✅] approved` | Include in APPLY |
| `[❌] skip` | Human decided to skip |
| `[🔍] needs-review` | Interesting but needs more investigation |

---

## Integration

**With `g-skl-harvest`**: `g-skl-harvest` runs ANALYZE + produces FEATURES.md for discovery. `g-skl-reverse-spec` is the same skill but focused on a single repo with deeper 5-pass coverage.

**With `g-skl-features`**: APPLY calls COLLECT to dedup against existing staging features.

**With `g-skl-vault`**: When vault is configured, write output to `{vault}/research/harvests/{slug}/` instead of project-local `research/harvests/`. (Task 081 — dedup + vault storage.)

**Reporter Rule — always enforced**:
> "We are documenting what this project does, not deciding what galdr needs. A feature being already present in galdr is NOT a reason to skip it — it's a reason to note the overlap and learn from the alternative approach."
