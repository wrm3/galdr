---
description: "Deep merge and analyze your own codebase projects"
---

# Command: @g-analyze-codebase

## Purpose
Deep merge two or more of YOUR OWN projects together. Full architectural integration with comprehensive task planning.

**This is for merging projects you own. For browsing external sources for ideas, use `@g-harvest` instead.**

## Usage
```
@g-analyze-codebase
```

Then provide the path to the codebase when prompted, or include it inline:
```
@g-analyze-codebase merge my project at research/my-other-project into this one
```

## This Command vs. @g-harvest

| | @g-analyze-codebase | @g-harvest |
|---|------------------------|---------------|
| **For** | Merging YOUR OWN projects | Browsing external sources for ideas |
| **Default** | Map everything for merge | Adopt nothing unless you choose |
| **Scope** | Comprehensive restructuring | Only what you pick from a menu |
| **Risk** | High (architectural) | Low (controlled) |

**Rule of thumb**: If you own both codebases and want to combine them, use this. If you're looking at someone else's work for ideas, use `@g-harvest`.

## Process

1. **Read the skill** at `.cursor/skills/codebase-integration-analysis/SKILL.md`
2. **Follow the 5-phase process** defined in the skill:
   - Phase 1: Codebase Exploration (launch 3-4 parallel explore agents)
   - Phase 2: Architecture Document creation
   - Phase 3: Comparison Document creation  
   - Phase 4: Integration Plan (new phase + tasks in TASKS.md)
   - Phase 5: Deliverables Verification

## Output Files

| File | Location |
|------|----------|
| Architecture Map | `docs/YYYYMMDD_HHMMSS_Cursor_{PROJECT}_ARCHITECTURE_MAP.md` |
| Comparison | `docs/YYYYMMDD_HHMMSS_Cursor_{PROJECT}_VS_GALDRWORKS_COMPARISON.md` |
| Phase File | `.galdr/phases/phase{N}_{project}-integration.md` |
| Tasks | `.galdr/TASKS.md` (updated with new phase and all tasks) |

## What Gets Analyzed

- **Every directory and subdirectory** of the external project
- **All configuration files** (.env, config files, CLI flags, defaults)
- **Entry points and data flow** through the system
- **API surfaces** (HTTP, WebSocket, CLI, IPC)
- **Extension/plugin architecture** if present
- **Security and auth mechanisms**

## What Gets Compared

- Feature-by-feature mapping against GaldrWorks
- Winner assessment with justification
- Priority gap table (HIGH/MEDIUM/LOW/SKIP)
- Settings/config parity check
- Unique features on both sides

## What Gets Planned

- New phase in `.galdr/TASKS.md` with proper ID range
- Tasks organized by category (verification, implementation, config, security, UI, docs)
- Each task sized for 1-4 hours
- Priority labels on every task
- Final verification and documentation tasks

## Quality Gates

Before completing, the system verifies:
- [ ] Architecture document covers ALL directories
- [ ] Comparison document covers ALL components  
- [ ] No settings/env vars missed
- [ ] Phase file created with proper YAML frontmatter
- [ ] TASKS.md updated with new phase and tasks
- [ ] Summary statistics updated
- [ ] Phase file and TASKS.md header are synchronized
- [ ] Documents follow `YYYYMMDD_HHMMSS_Cursor_TOPIC.md` naming

## Related Commands

| Command | When to Use After |
|---------|-------------------|
| `@g-plan` | Create detailed PRD for integration |
| `@g-task-new` | Create individual task spec files |
| `@g-task-update` | Update task status during work |
| `@g-review` | Review integration code |
| `@g-qa` | Track bugs found during integration |
| `@g-phase-sync-check` | Verify phase synchronization |
