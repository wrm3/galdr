# SUBSYSTEMS.md — {project_name}

## Overview
This document is the **master registry** of all subsystems in this project. Each subsystem has a detailed spec file in `.galdr/subsystems/{name}.md` — read the spec before modifying any subsystem.

**Rule**: Before making changes to any subsystem, read its spec file. This prevents architectural drift.

## Taxonomy

- **Subsystem** = engineering unit with its own code, config, state, and lifecycle
- **Sub-feature** = component documented within a parent subsystem's spec (not a separate entry here)
- **Integration** = external adapter listed under its host subsystem

Sub-features and integrations are documented in their parent's spec file, not as top-level entries.

## Subsystem Index

| Subsystem | Status | Spec File | Purpose |
|-----------|--------|-----------|---------|
| {subsystem-1} | {status} | `subsystems/{name}.md` | {purpose} |

<!-- Add subsystems as they are identified. Use @g-status or session-start sync to detect new ones. -->

## Sub-Features (documented in parent specs)

| Sub-Feature | Parent Subsystem | What It Covers |
|-------------|-----------------|----------------|

## Integrations (documented in parent specs)

| Integration | Host Subsystem | External System |
|-------------|---------------|-----------------|

## Interconnection Graph

```mermaid
graph TD
    %% Add subsystem nodes and edges as architecture develops
    %% Group related subsystems with subgraph blocks
```

## Dependency Summary

<!-- List subsystems grouped by dependency depth:
### No Dependencies (Foundation)
### Core Dependencies
### Data Layer
### Infrastructure
-->

---

**Last Updated**: {YYYY-MM-DD}
**Subsystem Count**: 0
