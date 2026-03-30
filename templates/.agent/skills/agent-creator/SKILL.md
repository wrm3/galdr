---
name: agent-creator
description: Create and configure AI agents for Cursor (.cursor/agents/) and Claude Agent SDK programmatic definitions.
---

# Agent Creator (Cross-Platform)

This skill provides guidance for creating AI agent definitions that work in **Cursor IDE** and the **Claude Agent SDK**.

## Platform Comparison

Agents work differently across platforms:

| Platform | Agent Location | Format | Discovery |
|----------|---------------|--------|-----------|
| **Cursor IDE** | `.cursor/agents/<name>.md` | Markdown file | Auto-discovered, selectable as subagent_type |
| **Claude Agent SDK** | Programmatic `AgentDefinition` | Python/TypeScript dict | Defined in code, invoked via Task tool |
| **Claude Code CLI** | No file-based agents | N/A | Uses Agent SDK or Skills instead |

**Source**: [Claude Agent SDK docs](https://platform.claude.com/docs/en/agent-sdk/overview)

### Key Difference

- **Cursor**: Agents are `.md` files in `.cursor/agents/`. Each defines a specialized persona that Cursor can invoke as a subagent.
- **Claude Agent SDK**: Agents are `AgentDefinition` objects with `description`, `prompt`, and `tools` fields. Invoked via the `Task` tool.
- **Claude Code CLI**: No native agent folder. Use Skills (`.claude/skills/`) for specialized knowledge, or the Agent SDK for programmatic agents.

## Cursor Agent Format (.cursor/agents/)

### File Location
```
.cursor/agents/
├── backend-developer.md
├── code-reviewer.md
├── database-expert.md
└── README.md
```

### Agent Template

```markdown
# Agent: {Agent Name}

## Role
{One-line role description}

## Expertise
- {Domain expertise 1}
- {Domain expertise 2}
- {Domain expertise 3}

## Responsibilities
- {What this agent does 1}
- {What this agent does 2}
- {What this agent does 3}

## Guidelines
- {How this agent should behave}
- {Quality standards to follow}
- {Patterns to use}

## Tools & Capabilities
- {Tools this agent should prefer}
- {File types this agent works with}

## Example Tasks
- "{Example user request 1}"
- "{Example user request 2}"
- "{Example user request 3}"
```

### Cursor Agent Best Practices

1. **Clear role definition** -- One sentence explaining what this agent specializes in
2. **Specific expertise** -- List concrete technical domains, not vague generalities
3. **Actionable guidelines** -- Include coding standards, patterns, and quality bars
4. **Tool preferences** -- Which MCP tools, languages, or frameworks this agent prefers
5. **Example tasks** -- 3-5 concrete examples of what users would ask this agent to do

### Cursor Agent Naming
- Filename: `kebab-case.md` (e.g., `backend-developer.md`)
- No special characters, no spaces
- Name should clearly describe the agent's role

## Claude Agent SDK Format

### AgentDefinition (Python)

```python
from claude_agent_sdk import AgentDefinition

agents = {
    "backend-developer": AgentDefinition(
        description="Backend development specialist for API design, server-side logic, and database integration.",
        prompt="""You are a backend development expert. Focus on:
- API design (REST, GraphQL)
- Server-side logic and business rules
- Database queries and schema design
- Error handling and logging
- Performance optimization

Follow these standards:
- Use type hints in Python
- Write comprehensive docstrings
- Use parameterized queries for all database operations
- Include error handling for all external calls""",
        tools=["Read", "Edit", "Bash", "Glob", "Grep"],
    )
}
```

### AgentDefinition (TypeScript)

```typescript
const agents = {
  "backend-developer": {
    description: "Backend development specialist for API design, server-side logic, and database integration.",
    prompt: `You are a backend development expert...`,
    tools: ["Read", "Edit", "Bash", "Glob", "Grep"],
  }
};
```

### Agent SDK Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | Short description shown to the orchestrating agent for deciding when to invoke |
| `prompt` | Yes | System instructions defining the agent's expertise and behavior |
| `tools` | Yes | List of tools this agent can use (Read, Edit, Bash, Glob, Grep, WebSearch, etc.) |

### Invoking SDK Agents

Agents are invoked via the `Task` tool:

```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep", "Task"],  # Task enables subagents
    agents=agents,
)
```

## Cross-Platform Agent Creation Process

### Step 1: Define the Role
- What is this agent's specialty?
- What makes it different from a general-purpose AI?
- What are 3-5 tasks only this agent should handle?

### Step 2: Define Expertise & Guidelines
- List specific technical domains
- Define coding standards and patterns
- Specify quality bars and review criteria
- List preferred tools and frameworks

### Step 3: Create for Cursor
Create `.cursor/agents/{agent-name}.md` using the Cursor template above.

### Step 4: Create for Agent SDK (Optional)
If the project also uses Claude Agent SDK, create the equivalent `AgentDefinition` in your Python/TypeScript code.

### Step 5: Cross-Reference with Skills
If this agent needs specialized knowledge, create a matching skill:
```
.cursor/skills/{agent-domain}/SKILL.md    # Detailed knowledge
.cursor/agents/{agent-name}.md             # Role definition
.claude/skills/{agent-domain}/SKILL.md     # Claude Code version
```

## Agent vs Skill -- When to Use Which

| Need | Use Agent | Use Skill |
|------|-----------|-----------|
| Define a **persona/role** | Yes | No |
| Package **domain knowledge** | No | Yes |
| Provide **step-by-step workflows** | No | Yes |
| Set **behavioral guidelines** | Yes | No |
| Bundle **scripts and references** | No | Yes |
| Create a **subagent type** for Task tool | Yes | No |

**Best practice**: Pair agents with skills. The agent defines the role; the skill provides the knowledge.

## Example: Creating a "Database Expert" Agent

### Cursor Version (.cursor/agents/database-expert.md)

```markdown
# Agent: Database Expert

## Role
Database specialist for schema design, query optimization, migrations, and data integrity.

## Expertise
- SQL query optimization (Oracle, PostgreSQL, MySQL)
- Schema design and normalization
- Migration planning and execution
- Index strategy and performance tuning
- Data integrity and constraint design

## Responsibilities
- Design and review database schemas
- Optimize slow queries with EXPLAIN analysis
- Plan and execute schema migrations
- Implement proper indexing strategies
- Ensure referential integrity

## Guidelines
- Always use parameterized queries (never string concatenation)
- Include EXPLAIN plans when optimizing queries
- Design for data integrity first, performance second
- Use migrations for all schema changes (never manual DDL)
- Document all non-obvious index choices

## Tools & Capabilities
- Prefers oracle_query and oracle_execute MCP tools
- Works with SQL, PL/SQL, migration scripts
- Uses EXPLAIN/EXPLAIN PLAN for optimization

## Example Tasks
- "Design a schema for user authentication"
- "This query is slow, can you optimize it?"
- "Create a migration to add a new column safely"
- "Review this schema for normalization issues"
```

### Agent SDK Version

```python
"database-expert": AgentDefinition(
    description="Database specialist for schema design, query optimization, migrations, and data integrity.",
    prompt="You are a database expert. Always use parameterized queries. Include EXPLAIN plans when optimizing. Design for integrity first, performance second.",
    tools=["Read", "Edit", "Bash", "Grep"],
)
```
