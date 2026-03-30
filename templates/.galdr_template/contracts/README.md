# .galdr/contracts/

This folder holds **shared contract specifications** between this project and its siblings or parents.

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

## File Format

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

1. **NOT in `docs/`** — docs may be gitignored; contracts must be gittracked
2. **Each project keeps its own copy** — local copies stay in sync via `@g-peer-sync`
3. **`canonical_owner` updates first** — the owner bumps the version; others sync after
4. **Sync via task** — contract updates create a `peer_sync` task in affected sibling projects

## Workflow

When you change a contract you own:
1. Update this file (bump version, update content)
2. Run `@g-peer-sync` to notify sibling projects
3. galdr creates peer_sync tasks in sibling projects' `.galdr/`

When a sibling notifies you their contract changed:
1. Check your INBOX.md for `[OPEN] SYNC-XXX` item
2. Run `@g-inbox` to action it
3. Update your local copy here
4. Mark the sync complete
