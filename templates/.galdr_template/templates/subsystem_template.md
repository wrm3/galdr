---
name: {subsystem-name}
status: active|planned|deprecated
owner: {team-or-person}
dependencies: [{other-subsystem-names}]
dependents: [{subsystems-that-depend-on-this}]
locations:
  code:
    - {path/to/main/source/files}
    - {path/to/additional/source}
  skills:
    - {.cursor/skills/relevant-skill/}
  agents:
    - {.cursor/agents/relevant-agent.md}
  commands:
    - {.cursor/commands/relevant-command.md}
  config:
    - {.galdr/config/relevant-config.md}
  db_tables:
    - {table_name (description)}
---

# {subsystem-name}

{One-paragraph description of what this subsystem does and why it exists.}

## Responsibility
- {Primary responsibility}
- {Secondary responsibility}
- {Additional responsibilities}

## Data Flow
```
{Input source} → {processing step} → {output/storage}
    ↓
{Next step in the pipeline}
```

## Key Files
| File | Purpose |
|------|---------|
| `{path}` | {what it does} |

## Sub-Features (if any)

### {Sub-Feature Name}
Skills: {skill-name}
{Brief description of the sub-feature and what it covers.}

## Architecture Rules
- {Non-negotiable constraint}
- {Design decision and rationale}

## When to Modify
- {Trigger condition for changes}
- {Another trigger condition}
