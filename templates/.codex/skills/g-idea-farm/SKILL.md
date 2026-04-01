---
name: g-idea-farm
description: >-
  Proactive codebase scanning for improvement opportunities — refactoring candidates,
  dead code, duplication, simplification targets, and feature ideas. Feeds
  IDEA_BOARD.md automatically. Runs daily via heartbeat or on-demand.
---

# g-idea-farm

Scan the codebase for improvement opportunities and add them to IDEA_BOARD.md.

## When to Use

- Daily scheduled scan via heartbeat (`daily-ideas` routine)
- Manual trigger: `@g-idea-farm`
- When looking for refactoring or simplification opportunities

## Scan Passes

Execute all 5 passes, collecting ideas. Limit to 10 new ideas per run.

### Pass 1: Code Simplification

Scan for complexity signals:
- Files > 500 lines: suggest extraction/splitting
- Functions > 50 lines: suggest decomposition
- Deeply nested code (> 4 levels of indentation): suggest flattening
- Repeated patterns across files: suggest abstraction

Tools: `rg`, `wc -l`, file analysis

### Pass 2: Dead Code Detection

Scan for unused code:
- Unused imports (grep for imports, check usage in other files)
- Functions/classes not referenced elsewhere in the codebase
- Commented-out code blocks > 10 lines
- Feature flags that are always on/off

Be conservative — false positives are worse than missed dead code.

### Pass 3: Duplication Analysis

Scan for repeated patterns:
- Similar function signatures across files
- Copy-pasted blocks (structural similarity)
- Skills/rules with overlapping content (galdr-specific)
- Repeated error handling patterns that could be centralized

### Pass 4: Improvement Ideas

Scan for missing best practices:
- Missing error handling (bare except, empty catch)
- Missing type hints (Python) or types (TypeScript)
- Missing tests for recently changed files
- Performance opportunities (N+1 patterns, unnecessary loops)
- Accessibility improvements for UI code

### Pass 5: Vault & External Knowledge

Cross-reference with project knowledge:
- Check vault for relevant research that hasn't been applied
- Check IDEA_BOARD.md for ideas that now have unblocked dependencies
- Cross-reference with PROJECT_GOALS.md for alignment opportunities

## Output Format

Add new entries to `.galdr/tracking/IDEA_BOARD.md`:

```markdown
### IDEA-NNN: {Title}
- **Source**: idea-farm (YYYY-MM-DD)
- **Category**: refactor|simplify|performance|security|feature|test
- **Effort**: low|medium|high
- **Impact**: low|medium|high
- **Files**: `{path}` (lines N-M)
- **Rationale**: {Why this improvement matters}
- **Status**: new
```

Also write a summary to `.galdr/logs/idea-farm/YYYY-MM-DD_idea_farm.md`.

## Deduplication

Before adding an idea:
1. Read existing IDEA_BOARD.md entries
2. Check if a similar idea already exists (same file + same category)
3. If duplicate: skip (don't re-add)
4. If related but different: add with reference to existing idea

## KPI Metrics

After scan, log to KPI system:
- `ideas_generated`: count of new ideas added
- `duplicates_skipped`: count of ideas skipped as duplicates
- `ideas_promoted`: count of ideas promoted to tasks (if any)

## Integration

- Heartbeat routine: `daily-ideas` (noon daily)
- Ideas are suggestions — user curates and promotes to tasks
- Each idea gets effort/impact estimates for prioritization
- Limit 10 new ideas per run to avoid overwhelming the board
