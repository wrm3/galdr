Broadcast a task to child projects with cascade depth: $ARGUMENTS

## What This Command Does

As a parent project, creates the same task in one or more child projects' `.galdr/` folders. Writes the task file, updates their TASKS.md, and adds an INBOX notification. Use when a change in this project requires action in dependent projects.

## Cascade Depth

- **Depth 1** (default): Creates tasks in immediate children only.
- **Depth 2**: Children also forward the task to their children (grandchildren receive it on next session open).
- **Depth 3**: Three generations — grandchildren forward to great-grandchildren.

Children forward automatically on their next session open (Step 7 of session start protocol).

## Targeting

- All children (default)
- Children that consume a specific service: "broadcast to all oracle consumers"
- Specific projects by name: "broadcast to payments-service and card-service only"

## What Gets Created

In each target child project:
- A task file in `.galdr/tasks/` with cross-project YAML metadata
- An INBOX entry in `.galdr/linking/INBOX.md`
- An entry in their TASKS.md

In this project:
- An optional broadcast tracking task

## Example Usage

"Broadcast: Oracle Bifrost is upgrading to v2. All oracle consumers need to update their connection code. Depth 2."

Follows the `g-broadcast` skill.
