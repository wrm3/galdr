View or edit this project's cross-project topology: $ARGUMENTS

## What This Command Does

Reads `.galdr/PROJECT_TOPOLOGY.md` and displays the current project's declared relationships — parents, children, and siblings. Use this to add new relationships or verify existing ones.

## When to Use

- **Starting cross-project work** — see who this project depends on or who depends on it
- **Adding a new relationship** — "add core-platform as a parent" or "add payments-service as a sibling"
- **Verifying paths** — confirm that related project paths are accessible from this workspace
- **First time setup** — after `@g-setup`, declare your project's place in the ecosystem

## What Gets Shown

```
PROJECT: payments-service — payments-service
Layer:   domain_service

Parents:  core-platform (../core-platform) — consumes: jwt_auth, rbac, oracle_bridge
Children: ach-ui (../ach-ui)
Siblings: card-service (../card-service) — contracts: oracle_connection_protocol
          api-gateway (../api-gateway) — contracts: cbs_api_interface
Contracts: .galdr/contracts/oracle_connection_protocol.md
           .galdr/contracts/cbs_api_interface.md
```

## Editing Relationships

Say things like:
- "Add core-platform as parent, I consume jwt_auth and rbac"
- "Add ach-ui as a child, I provide api_endpoints"
- "Add card-service as sibling with a shared oracle contract"

Follows the `g-topology` skill.
