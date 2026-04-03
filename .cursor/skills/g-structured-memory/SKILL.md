---
name: g-structured-memory
description: >-
  Categorized agent memory with scope, confidence, and provenance. Upgrades flat
  "Learned Workspace Facts" to structured tables. Integrates with g-continual-learning
  for smarter fact management.
---

# g-structured-memory

Manage structured agent memory entries with categories, scope, confidence scores, and provenance tracking.

## When to Use

- When adding new workspace facts (automatic via g-continual-learning)
- When migrating existing flat facts to structured format
- When querying memory by category or scope
- When reviewing fact confidence and staleness

## Memory Categories

| Category | Prefix | Description |
|----------|--------|-------------|
| Constraints | C-NNN | Hard rules that must never be violated |
| Preferences | P-NNN | User/team preferences for how things should be done |
| Patterns | T-NNN | Recurring technical patterns observed across sessions |
| Decisions | D-NNN | Architectural or design decisions with rationale |

## Structured Format

Facts are stored in AGENTS.md and CLAUDE.md under `## Learned Workspace Facts`:

```markdown
## Learned Workspace Facts

### Constraints
| # | Fact | Scope | Confidence | Source | Date |
|---|------|-------|------------|--------|------|
| C-001 | Docker never touches the vault filesystem | global | 0.95 | user | 2026-03-29 |

### Preferences
| # | Fact | Scope | Confidence | Source | Date |
|---|------|-------|------------|--------|------|
| P-001 | Use UV for Python, never pip or venv directly | global | 0.95 | user | 2026-02-15 |

### Patterns
| # | Fact | Scope | Confidence | Source | Date |
|---|------|-------|------------|--------|------|
| T-001 | 8-target propagation for skills/hooks/rules | project | 0.90 | decision | 2026-03-29 |

### Decisions
| # | Fact | Scope | Confidence | Source | Date |
|---|------|-------|------------|--------|------|
| D-001 | WebSocket sync is single-user multi-machine only | project | 0.90 | decision | 2026-03-29 |
```

## Scope

- **global**: Applies to ALL projects using galdr. Goes in both AGENTS.md and CLAUDE.md.
- **project**: Applies only to this project.

Determination rules:
- User says "always" / "never" / "from now on" -> global
- Fact references specific files/subsystems -> project
- Architectural decisions -> project (unless cross-project)

## Confidence Lifecycle

| Event | Confidence Change |
|-------|-------------------|
| New fact (single occurrence) | 0.50 |
| Confirmed by user correction | +0.15 |
| Repeated in another session | +0.10 |
| Contradicted by user | -0.30 |
| Not referenced in 90 days | -0.05/month |
| Confidence < 0.20 | Candidate for removal |
| Confidence > 0.90 | Promoted to rule candidate |

## Source Types

| Source | Meaning |
|--------|---------|
| user | Direct user statement |
| correction | User corrected agent behavior |
| decision | Architectural decision during planning |
| pattern | Agent observed recurring pattern |
| self | Agent inferred from codebase analysis |

## Adding a New Fact

1. Determine category (constraint/preference/pattern/decision)
2. Determine scope (global/project)
3. Set initial confidence based on source:
   - `user`/`correction`: 0.70
   - `decision`: 0.80
   - `pattern`/`self`: 0.50
4. Check for contradictions with existing facts
5. If contradiction: decrease old fact confidence by 0.30, add new fact
6. If duplicate: increase existing fact confidence by 0.10
7. Assign next available ID in category (C-NNN, P-NNN, T-NNN, D-NNN)
8. Append to appropriate table in AGENTS.md and CLAUDE.md

## Migration from Flat Format

Run the migration script to convert existing numbered facts:

```bash
python .cursor/skills/g-structured-memory/scripts/migrate_facts.py
```

The script:
1. Reads current `## Learned Workspace Facts` section
2. Categorizes each entry (keyword-based heuristics)
3. Assigns scope (most existing facts are project-scoped)
4. Sets confidence to 0.85 (established facts)
5. Rewrites section in structured table format
6. Preserves all existing content (no data loss)

## Backward Compatibility

Agents that don't understand the table format can still read facts as plain text. The table headers and pipe separators are valid Markdown and render correctly in all platforms.
