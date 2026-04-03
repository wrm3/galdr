---
name: g-review-heartbeat
description: >-
  Automated code review on recent git changes. Incremental — only reviews files
  changed since the last review. Produces severity-rated findings report.
  Runs daily via heartbeat or on-demand.
---

# g-review-heartbeat

Perform automated code review on files changed since the last review.

## When to Use

- Daily/weekly scheduled review via heartbeat (`daily-code-review` routine)
- Manual trigger: `@g-review-heartbeat`
- After a batch of commits to catch issues before they accumulate

## Workflow

### Step 1: Determine Review Scope

1. Read `.galdr/logs/reviews/last_review_commit.txt` for the last reviewed commit hash
2. If file doesn't exist, use `HEAD~7` as the starting point
3. Run `git diff {last_commit}..HEAD --name-only` to get changed files
4. Filter out:
   - `.galdr/` management files
   - Lock files (`*.lock`, `package-lock.json`, `uv.lock`)
   - Generated files (`.min.js`, `.map`, `dist/`)
   - Binary files
   - Files > 2000 lines (review in chunks if needed)

### Step 2: Review Each File

For each changed file, analyze for:

**Security**
- Hardcoded credentials, API keys, tokens
- SQL injection vectors (string concatenation in queries)
- Unvalidated user input
- Insecure deserialization
- Missing authentication/authorization checks

**Quality**
- Functions > 50 lines
- Deeply nested code (> 4 levels)
- Missing error handling (empty catch blocks, bare except)
- Unused imports/variables
- Inconsistent naming conventions

**Performance**
- N+1 query patterns
- Unnecessary loops or repeated computation
- Missing caching opportunities
- Large memory allocations in loops

**Maintainability**
- Missing type hints (Python) or types (TypeScript)
- Complex boolean expressions without explanation
- Magic numbers without constants
- Duplicated code blocks

### Step 3: Aggregate Findings

Rate each finding:
- **Critical**: Security vulnerabilities, data loss risks
- **Medium**: Quality issues, performance problems
- **Low**: Style suggestions, minor improvements

### Step 4: Write Report

Output to `.galdr/logs/reviews/YYYY-MM-DD_code_review.md`:

```markdown
---
date: YYYY-MM-DD
type: code_review
commits_reviewed: {start_hash}..{end_hash}
files_reviewed: N
findings: N critical, N medium, N low
trigger: scheduled|manual
---

# Code Review — YYYY-MM-DD

## Critical Findings
### [CR-001] {Title} ({file}:{line})
- **Severity**: Critical
- **Category**: Security|Quality|Performance|Maintainability
- **File**: `{path}`
- **Action**: {What to do}

## Medium Findings
...

## Low Findings / Suggestions
...

## Summary
| Category | Count |
|----------|-------|
| Security | N |
| Performance | N |
| Maintainability | N |
| Style | N |
```

### Step 5: Update Tracking

1. Write current HEAD hash to `.galdr/logs/reviews/last_review_commit.txt`
2. If critical findings exist, add entry to `.galdr/config/WAKEUP_QUEUE.md`

## KPI Metrics

After review, log to KPI system:
- `files_reviewed`: count of files analyzed
- `findings_critical`: count of critical findings
- `findings_medium`: count of medium findings
- `findings_total`: total findings across all severities

## Integration

- Heartbeat routine: `daily-code-review` (weekdays 8:00 PM)
- Leverages existing `g-review` skill for review logic
- Incremental: only reviews changes since last review
- Critical findings trigger WAKEUP_QUEUE entry for user attention
