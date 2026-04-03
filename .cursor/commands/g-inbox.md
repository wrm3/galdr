Review and action cross-project coordination items: $ARGUMENTS

## What This Command Does

Opens `.galdr/linking/INBOX.md` and walks through all pending items — conflicts, parent broadcasts, child requests, and sibling peer syncs. Resolves conflicts, creates tasks for actionable items, and marks done items as complete.

## Priority Order

1. **⚠️ CONFLICTS** — Two parents gave incompatible instructions. Must resolve before planning work on the affected subsystem.
2. **📨 REQUESTS** — Child projects are asking this project to do something (e.g., "add me to VALID_SYSTEMS").
3. **📢 BROADCASTS** — Parent projects sent tasks to be done here. Tasks should already exist.
4. **🔄 PEER SYNCS** — Sibling projects updated a shared contract. Local copy needs updating.

## Key Behaviors

- Conflicts are resolved by **you** — the AI will never auto-resolve them
- Requests create real tasks in `.galdr/tasks/` and notify the requesting child
- Peer syncs are advisory — work proceeds; sync when convenient
- All resolutions are recorded in INBOX.md for audit trail

## When to Run

- Any time after session start shows `INBOX: N open` items
- After a `@g-broadcast` was sent and you want to confirm child delivery
- After receiving a `peer_sync` notification from a sibling

Follows the `g-inbox` skill.
