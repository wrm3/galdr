# .galdr/linking/

Cross-project coordination hub — shared contracts, inbox, and peer-sync artifacts.

## What's In This Folder

| File | Purpose |
|------|---------|
| `INBOX.md` | Incoming coordination items from parent/child/sibling projects |
| `*.md` (contract files) | Shared interface specifications between sibling projects |
| `README.md` | This file |

## INBOX.md

The inbox receives items from connected projects via `@g-broadcast`, `@g-request`, and `@g-peer-sync`.

Item types: `[REQUEST]`, `[BROADCAST]`, `[SYNC]`, `[CONFLICT]`

`[CONFLICT]` items block planning until resolved.

## What Is a Contract?

A contract is a shared specification that, if one project changes it, breaks another project. Examples:

| Contract Type | Example |
|---|---|
| API shape | Request/response format between two services |
| Database schema | Shared table structure two projects read/write |
| Event format | Message queue payload agreed by producer + consumer |
| Auth claims | JWT fields expected by multiple consumers |
| File format | Output file from one project consumed by another |
| Config schema | Shared config format parsed by multiple projects |

## Contract File Format

Each contract file uses YAML frontmatter:

```markdown
---
contract_name: my_contract
version: 1.0
canonical_owner: other-project-id   # who maintains the source of truth
parties: [this-project, other-project]
last_synced: YYYY-MM-DD
sync_status: current                 # current | needs_review | conflict
---

# Contract Name — v1.0

[Specification content here]
```

## Rules

1. **Each project keeps its own copy** — local copies stay in sync via `@g-peer-sync`
2. **`canonical_owner` updates first** — the owner bumps the version; others sync after
3. **Sync via task** — contract updates create a `peer_sync` task in affected sibling projects

## Workflow

When you change a contract you own:
1. Update the contract file here (bump version, update content)
2. Run `@g-peer-sync` to notify sibling projects
3. galdr creates peer_sync tasks in sibling projects' `.galdr/`

When a sibling notifies you their contract changed:
1. Check `INBOX.md` for `[OPEN] SYNC-XXX` item
2. Run `@g-inbox` to action it
3. Update your local copy here
4. Mark the sync complete
