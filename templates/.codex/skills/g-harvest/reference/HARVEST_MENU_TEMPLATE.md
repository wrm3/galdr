# Harvest Menu Template

Use this template when presenting harvest suggestions to the user.

---

## Harvest Menu: {Source Name}

**Source Type**: {Repository / Article / Video Transcript / Research Paper / Other}
**Source Location**: {path, URL, or reference}
**Analyzed**: {date}

**Project Context Loaded**:
- Mission: {from PROJECT_CONTEXT.md}
- Active Phase: {from TASKS.md}
- Subsystems: {count} active

---

### Category: {Category Name}

**H-01: {Short Descriptive Title}**
- **What it is**: {2-3 sentences explaining the capability, pattern, or idea}
- **Where in source**: {file path, section heading, or timestamp}
- **How it helps us**: {1-2 sentences on specific benefit to OUR project}
- **Effort estimate**: {Small (< 4 hours) / Medium (1-2 days) / Large (3+ days)}
- **Affects subsystems**: {list of our subsystems that would change}
- **Risk**: {Low / Medium / High} -- {brief justification}
- **Overlaps with**: {existing TASKS.md item if any, or "None"}

---

### Summary Table

| # | Suggestion | Effort | Risk | Category | Overlap |
|---|-----------|--------|------|----------|---------|
| H-01 | {title} | Small | Low | {cat} | None |
| H-02 | {title} | Medium | Low | {cat} | Task 205 |
| H-03 | {title} | Large | Medium | {cat} | None |

**Total suggestions**: {count}
**Quick wins (Small effort + Low risk)**: {count}
**Overlaps with existing planned work**: {count}

---

### Recommended Groupings

Items that work well together:
- **Group A**: H-01 + H-04 (both improve {area})
- **Group B**: H-03 depends on H-02 (do H-02 first)

### Items to Consider Carefully

- **H-{XX}**: {reason for caution -- high risk, large effort, architectural impact}

---

**Your turn.** Reply with:
- Numbers you want (e.g., "H-01, H-03, H-07")
- "tell me more about H-{XX}" for details
- "none" to pass on all
- Or discuss any item you want to modify

---

## After User Selection

### Approved Items Summary

| # | Suggestion | Effort | Decision |
|---|-----------|--------|----------|
| H-01 | {title} | Small | Approved |
| H-02 | {title} | Medium | Rejected |
| H-03 | {title} | Large | Approved (modified: {user's modification}) |
| H-04 | {title} | Small | Deferred |

**Approved**: {count} items
**Estimated total effort**: {range}
**Target phase**: {existing Phase N / New Phase}

Proceeding to create tasks for approved items only.
