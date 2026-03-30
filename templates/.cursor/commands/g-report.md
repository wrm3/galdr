Project backlog and status report: $ARGUMENTS

## What This Command Does

Generates a detailed operational report covering commit history, task availability, and all blockers across the project. Designed for quick situational awareness — everything you need to decide what to work on next.

## Report Sections

### 1. Last Commit Information

Run and display:
```powershell
git log -1 --format="Commit: %h%nAuthor: %an%nDate: %ai%nMessage: %s"
git log -1 --format="%ar"   # relative time ("3 hours ago")
```

Also check:
```powershell
git status --short           # Any uncommitted changes?
git stash list               # Any stashed work?
```

Present as:
```markdown
## Last Commit
- **Hash**: abc1234
- **When**: 3 hours ago (2026-03-18 14:30)
- **Author**: {name}
- **Message**: {commit message}
- **Uncommitted changes**: {count} files modified, {count} untracked
- **Stashed work**: {count} stashes
```

### 2. Available Tasks (Ready to Work)

From TASKS.md, find all tasks that are **immediately workable**:
- Status: `[ ]` (pending) or `[📋]` (ready)
- All dependencies satisfied (prerequisite tasks completed)
- Not blocked by human input or external factors

Group by priority:

```markdown
## Available Tasks ({total} ready to work)

### Critical Priority ({count})
- [ ] #{id}: {title} — Phase {N}

### High Priority ({count})
- [ ] #{id}: {title} — Phase {N}

### Medium Priority ({count})
- [ ] #{id}: {title} — Phase {N}

### Low Priority ({count})
- [ ] #{id}: {title} — Phase {N}
```

### 3. In-Progress Tasks

Tasks currently being worked on:

```markdown
## In-Progress ({count})
- [🔄] #{id}: {title} — claimed by {agent/human}, started {when}
```

### 4. Blocked Tasks (Comprehensive Breakdown)

Categorize EVERY non-available, non-completed task by blocker type:

```markdown
## Blocked Tasks ({total} blocked)

### Needs Human Input ({count})
Tasks requiring a decision, clarification, or manual action:
- #{id}: {title} — {what human input is needed}

### Blocked by Prerequisites ({count})
Tasks waiting on other incomplete tasks:
- #{id}: {title} — waiting on #{dep_id} ({dep_status})

### Missing Information / Unclear Spec ({count})
Tasks with incomplete or ambiguous specifications:
- #{id}: {title} — {what's unclear}

### External Dependencies ({count})
Tasks blocked by something outside the codebase:
- #{id}: {title} — {external blocker: API access, credentials, third-party service}

### Failed / Needs Retry ({count})
Tasks that were attempted and failed:
- #{id}: {title} — failed because {reason}

### Awaiting Verification ({count})
Completed but not yet verified:
- #{id}: {title} — implemented by {who}, needs verification
```

### 5. Progress Summary

```markdown
## Progress Overview

| Status | Count | % |
|--------|-------|---|
| Completed | {n} | {%} |
| In-Progress | {n} | {%} |
| Available (Ready) | {n} | {%} |
| Blocked | {n} | {%} |
| Failed | {n} | {%} |
| **Total** | **{n}** | **100%** |

Phase Progress:
- Phase {N} "{name}": {completed}/{total} tasks ({%}%)
- Phase {M} "{name}": {completed}/{total} tasks ({%}%)
```

### 6. Recommendations

Based on the analysis, suggest:

```markdown
## Recommended Actions
1. **Work next**: #{id} — {title} ({priority}, unblocked)
2. **Unblock**: #{id} needs {specific action} to become available
3. **Review**: #{id} is awaiting verification
4. **Commit**: {if uncommitted changes exist, suggest committing}
```

## Report Filtering

If `$ARGUMENTS` specifies a scope:
- `phase 2` — only show Phase 2 tasks
- `blocked` — only show the blocked tasks section
- `available` — only show available tasks
- `critical` — only show critical priority items
- `brief` — condensed single-screen summary

## When to Use

- Start of a work session ("what should I work on?")
- Before running `@g-go` (understand the landscape)
- Standup preparation
- Checking if anything became unblocked
- End of session review

Let's see what we're working with.
