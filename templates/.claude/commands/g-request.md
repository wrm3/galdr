Request action from a parent project: $ARGUMENTS

## What This Command Does

As a child project, formally requests that a parent project perform an action (e.g., add this project to VALID_SYSTEMS, insert a nav menu item, create an API key). Creates a local blocked task and writes a request to the parent's `INBOX.md`.

## What Gets Created

In **this project**:
- A task in `.galdr/tasks/` with `status: blocked` and `requires_parent_action: true`
- An entry in `TASKS.md`

In the **parent project** (if path accessible):
- An `[OPEN] REQ-XXX` entry in their `INBOX.md`

If parent is not accessible: the request is staged in `.galdr/pending_requests/` for manual delivery.

## When to Use

- You need the parent to add you to a registry (VALID_SYSTEMS, nav menu, service list)
- You need the parent to create a resource (API key, database user, Gitea repo)
- You need the parent to make a code change in shared infrastructure
- You're blocked and can't proceed until the parent acts

## Key Behavior

- Your local task stays `blocked` until parent marks `parent_action_status: completed`
- The blocked task appears as an **advisory** in `@g-status` — it doesn't stop other work
- Parent sees it prominently in their `@g-inbox` on next session open

## Example Usage

"Request core-platform to add payments-service to VALID_SYSTEMS in postgres.py — blocking my PostgreSQL discovery feature."

Follows the `g-request` skill.
