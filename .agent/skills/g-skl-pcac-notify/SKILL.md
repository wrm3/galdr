---
name: g-skl-pcac-notify
description: Send lightweight [INFO] freeform notifications to one or more project INBOXes — no task created, no approval needed. FYI-only cross-project messaging.
---

# g-skl-pcac-notify — PCAC Freeform Notifications

## When to Use

When you want to say "FYI" across project boundaries without creating a task or request:
- "I renamed API endpoint X"
- "T024 is done — might affect your timeline"
- "I found a pre-existing bug in the shared contract, not blocking"

**INFO messages**: no task created, no approval needed, no local task blocked.

## INFO Message Format

Written to target project's `.galdr/linking/INBOX.md`:

```markdown
## [OPEN] INFO-{NNN} — from: {source_project} — {YYYY-MM-DD}
**Type:** info
**Subtype:** {general | broadcast_completion | advisory}
**Subject:** {one-line description}
**Detail:** {optional multi-line context}
**Action required:** none
**Status:** unread
```

## Routing Options

| Flag | Target |
|------|--------|
| `--project <path>` | Single project by path |
| `--parent` | Parent project (from PROJECT.md Project Linking section) |
| `--all-children` | All child projects in topology |
| `--all-siblings` | All sibling projects |

Multiple flags are allowed: `--parent --all-siblings` notifies parent and all siblings.

## Steps

1. **Identify target project(s)** from the routing flag
2. **Draft the INFO entry** using the format above
   - Assign next INFO-NNN ID (scan target INBOX for highest existing INFO-NNN, increment)
   - Subtype: `general` (default), `broadcast_completion` (T037), or `advisory`
3. **Write to target INBOX.md** (append at top, after the header)
   - If target path is accessible: write directly
   - If target path is NOT accessible: stage in `.galdr/linking/pending_requests/info_[target].md`
     (same staging pattern as g-skl-pcac-ask)
4. **Read back to confirm** the entry was written
5. **Report**: "Notified [project_name]: INFO-NNN — {subject}"

## Staging When Target Inaccessible

```
.galdr/linking/pending_requests/info_[target_project_name].md
```

Staged notifications are delivered the next time any PCAC command accesses that project.

## What This Does NOT Do

- Does NOT create a task in the source project
- Does NOT create a task in the target project
- Does NOT block anything
- Does NOT require the receiver to take action
- Does NOT trigger the CONFLICT gate in g-skl-pcac-order

## Usage Examples

```
@g-pcac-notify --parent "Completed T024 subsystem rename — all subsystem names updated"
@g-pcac-notify --all-siblings "New g-skl-learn skill available via template propagation"
@g-pcac-notify --project /path/to/sibling "Bug found in shared API contract (non-blocking, will fix T036)"
```
