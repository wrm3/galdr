---
description: "Automated code review on recent changes since last review"
---

# g-review-heartbeat

Review code changes since the last review.

## Behavior

1. Read the `g-review-heartbeat` skill at `.cursor/skills/g-review-heartbeat/SKILL.md`
2. Determine review scope from last_review_commit.txt
3. Review changed files for security, quality, performance, maintainability
4. Write report to `.galdr/logs/reviews/YYYY-MM-DD_code_review.md`
5. Update last_review_commit.txt
