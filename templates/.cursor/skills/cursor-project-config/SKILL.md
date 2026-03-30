---
name: cursor-project-config
description: Maintain .cursor/ IDE config — rules, agents, skills, commands, mcp.json, numbering, and official-docs sync.
---

# Cursor IDE Project Configuration

Create, maintain, audit, and update `.cursor/` project configurations. Self-updating — checks official docs for latest features before making changes.

## Self-Update Protocol

**Before making any structural changes to .cursor/, always check the latest docs:**

1. Fetch https://docs.cursor.com/context/rules — Rules documentation
2. Fetch https://docs.cursor.com/context/context-types — Context types
3. Fetch https://docs.cursor.com/chat/agents — Agent mode docs
4. Fetch https://docs.cursor.com/context/model-context-protocol — MCP docs
5. Fetch https://docs.cursor.com/troubleshooting/troubleshooting — Known issues

Compare fetched content against `reference/cursor_structure.md`. If any new features, file formats, or settings are found, update the reference file AND this SKILL.md before proceeding.

## Complete .cursor/ Structure

```
project-root/
├── .cursorrules                   # Legacy single-file rules (deprecated)
│
└── .cursor/
    ├── mcp.json                   # MCP server configuration
    ├── rules/                     # Numbered .mdc rule files
    │   ├── README.md              # Numbering convention docs
    │   └── {NN}_{name}.mdc       # Rules with YAML frontmatter
    ├── agents/                    # Agent definitions
    │   ├── README.md
    │   └── {agent-name}.md       # YAML frontmatter + markdown
    ├── commands/                  # Slash commands
    │   └── {command-name}.md     # $ARGUMENTS substitution
    └── skills/                    # Skill directories
        └── {skill-name}/
            ├── SKILL.md           # Required
            ├── reference/         # Documentation
            ├── scripts/           # Executable code
            └── assets/            # Output resources
```

## Rules — .cursor/rules/*.mdc

### File Format

```yaml
---
description: 'Brief description for rule picker'
globs:
  - '**/*.py'
  - '**/*.ts'
alwaysApply: false
---

# Rule Content (Markdown)
```

### Frontmatter Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `description` | string | Yes | Brief text shown in rule picker |
| `globs` | array | No | File patterns to auto-activate |
| `alwaysApply` | boolean | Yes | true = always loaded, false = on-demand |

### Numbering Convention

```
00-09: Universal (always, docs, git, code review)
10-19: App-specific core (task mgmt, planning, QA)
20-29: Reserved
30-39: Platform (PowerShell, curl, Python venv)
40-49: Database / RAG
50-59: DevOps (CI/CD, K8s, Portainer)
60-69: Business (product dev, resources)
70-79: Workflows (parallel execution)
80-89: Domain-specific (3D, ML, etc.)
```

### Creating a New Rule

1. Choose number range based on category
2. Create `{NN}_{descriptive_name}.mdc`
3. Add frontmatter (description, globs, alwaysApply)
4. Write rule content in Markdown
5. Update `.cursor/rules/README.md`

## Agents — .cursor/agents/*.md

```yaml
---
name: agent-name
description: One-line description for agent picker
tools: Read, Edit, Write, Bash, Grep, Glob
model: sonnet
---

# Agent Name

## Purpose
[What this agent specializes in]

## Expertise Areas
[Bulleted list]

## Instructions
[Step-by-step workflow]

## When to Use
[Trigger conditions]
```

| Field | Required | Values |
|---|---|---|
| `name` | Yes | kebab-case identifier |
| `description` | Yes | One-line purpose |
| `tools` | Yes | Comma-separated tool list |
| `model` | Yes | sonnet, opus, haiku |

## Skills — .cursor/skills/*/SKILL.md

```yaml
---
name: skill-name
description: Comprehensive description
triggers:
  - "keyword 1"
  - "keyword 2"
agents:
  - agent-name
version: 1.0.0
---

# Skill Title
[Content with decision trees, code examples, troubleshooting]
```

### Cursor-Specific Fields

| Field | Purpose |
|---|---|
| `triggers` | Keywords that auto-activate this skill |
| `agents` | Which agents can use this skill |
| `version` | Semantic version for tracking |

## Commands — .cursor/commands/*.md

```markdown
Command description: $ARGUMENTS

## What This Command Does
[Explanation]

## Workflow
### 1. [Step]
[Details]

## What I Need From You
[Required input]
```

No YAML frontmatter. `$ARGUMENTS` is replaced with user input when invoked.

## MCP — .cursor/mcp.json

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"]
    }
  }
}
```

## Context Budget Management

```
Total: ~200K tokens per conversation
Rules:         <2% (~4K tokens) — keep files <100 lines
MCP tools:     ~8%
Conversation:  ~18%
Skills:        Lazy-loaded as needed
```

**Guidelines:**
- Keep rule files under 100 lines
- Mission-critical rules can be up to 500 lines
- Skills have complete details; rules are reminders/pointers
- Heavy reference material goes in `skills/*/reference/`

## Maintenance Workflows

### Audit Existing Config
1. Read all `.mdc` files in `.cursor/rules/`
2. Verify frontmatter (description, globs, alwaysApply)
3. Check numbering gaps and ordering
4. Verify all agents have required frontmatter fields
5. Check skills have SKILL.md with proper schema
6. Report findings

### Add New Rule
1. Determine category → number range
2. Find next available number in range
3. Create `{NN}_{name}.mdc` with frontmatter
4. Update `rules/README.md`

### Add New Agent
1. Create `.cursor/agents/{name}.md`
2. Include frontmatter: name, description, tools, model
3. Mirror to `.claude/agents/` if dual-platform project

### Add New Skill
1. Create `.cursor/skills/{name}/SKILL.md`
2. Include frontmatter: name, description, triggers, agents, version
3. Add `reference/` directory if needed
4. Mirror to `.claude/skills/`

### Sync .claude/ ↔ .cursor/
1. Diff agents between both directories
2. Diff skills between both directories
3. Report mismatches
4. Offer to sync (copy missing files, update outdated)

## Reference Files
- `reference/cursor_structure.md` — Full structure reference (self-updated from official docs)
