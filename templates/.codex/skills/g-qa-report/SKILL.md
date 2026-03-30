---
name: g-qa-report
description: Generate quality metrics — bug counts, resolution rates, severity, phase impact, health score.
---
# galdr-qa-report

## When to Use
@g-qa-report or "quality report" or "bug metrics". Generates current quality health snapshot.

## Steps

1. **Read BUGS.md**: parse all bug entries, group by severity and status

2. **Read TASKS.md**: identify all `[BUG]`-prefixed tasks, check completion

3. **Collect metrics**:
   - Total bugs: open / closed / in-progress
   - Severity distribution: critical/high/medium/low counts
   - Resolution rate: closed / total × 100
   - Average age (open bugs): days since created
   - Regression count: bugs introduced by a fix

4. **Phase impact analysis**: which phases have most bugs?

5. **Reusability metrics** (from code review history):
   - 3-strike violations detected
   - Shared modules created vs inline duplication

6. **Generate report**:
```markdown
# Quality Metrics Report
**Generated**: YYYY-MM-DD HH:MM
**Project**: [from PROJECT_CONTEXT.md]

## Bug Summary
| Metric | Value |
|---|---|
| Total Bugs | N |
| Open | N |
| In Progress | N |
| Closed | N |
| Resolution Rate | N% |

## Severity Distribution
| Severity | Open | Closed | Total |
|---|---|---|---|
| Critical | N | N | N |
| High | N | N | N |
| Medium | N | N | N |
| Low | N | N | N |

## Phase Impact
| Phase | Bug Count | Open |
|---|---|---|
| Phase 0 | N | N |
| Phase 1 | N | N |

## Quality Score
Score: N/100
Status: Healthy (≥80) | Degraded (50-79) | Critical (<50)

## Recommendations
- [Top priority fix]
- [Pattern to address]
```
