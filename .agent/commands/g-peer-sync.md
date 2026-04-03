Synchronize a shared contract with a sibling project: $ARGUMENTS

## What This Command Does

Initiates or responds to a contract synchronization between sibling projects. When you change a shared contract, notifies the sibling and creates tasks on both sides. When a sibling notifies you, helps you update your local copy.

## Contracts Live In `.galdr/linking/`

NOT in `docs/` — contracts are critical shared specifications that must be gittracked. Each project keeps its own copy. `@g-peer-sync` keeps copies aligned.

## Key Principle: Advisory Only

Peer syncs never block work. Your project proceeds regardless. The sync shows as an advisory in `@g-status` until resolved at a convenient time.

## Two Directions

**I changed a contract** (I am initiating):
1. Update my `.galdr/linking/<name>.md` (bump version, update content)
2. Notify sibling's INBOX.md
3. Create task in sibling's `.galdr/` (if path accessible)
4. Create local tracking task

**Sibling notified me** (I am responding):
1. Read sibling's updated spec
2. Update my local copy
3. Close the task and mark INBOX item done
4. Confirm back to sibling

## Example Usage

- "I updated the cbs_api_interface contract — notify api-gateway and card-service"
- "Respond to the peer sync from api-gateway for cbs_api_interface"
- "Check what contract syncs are pending with my siblings"

Follows the `g-peer-sync` skill.
