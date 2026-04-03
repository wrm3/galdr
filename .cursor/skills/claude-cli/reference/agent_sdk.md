# Agent SDK Reference

Python and TypeScript SDKs for programmatic Claude Code integration. Use these when building agents, automation pipelines, or custom tooling that invokes Claude Code as a library rather than a CLI process.

Official docs: https://docs.claude.com/en/api/agent-sdk/overview

---

## Python SDK

### Installation

```bash
pip install claude-agent-sdk
# or: uv add claude-agent-sdk
```

### Basic Usage

```python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        allowed_tools=["Read", "Edit", "Bash(npm test)"],
        model="sonnet",
        cwd="/path/to/project",
        max_turns=30,
    )

    async for message in query(
        prompt="Implement sorting algorithm with tests",
        options=options,
    ):
        if message.type == "assistant":
            print(message.content)
        elif message.type == "result":
            print(f"Done. Cost: ${message.cost_usd:.4f}")

anyio.run(main)
```

### ClaudeAgentOptions (Python)

| Field | Type | Description |
|-------|------|-------------|
| `permission_mode` | `str` | `"default"`, `"acceptEdits"`, `"bypassPermissions"` |
| `allowed_tools` | `list[str]` | Tools to pre-authorize (glob patterns supported) |
| `disallowed_tools` | `list[str]` | Tools to block |
| `model` | `str` | Model name (`"opus"`, `"sonnet"`, `"haiku"`) |
| `cwd` | `str` | Working directory |
| `max_turns` | `int` | Maximum agentic turns |
| `max_budget_usd` | `float` | Spending cap in USD |
| `system_prompt` | `str` | Replace default system prompt |
| `append_system_prompt` | `str` | Append to default system prompt |
| `mcp_config` | `str` | Path to MCP config file |
| `agents` | `dict` | Subagent definitions (same as `--agents` JSON) |

### Message Types

| Type | Fields | Description |
|------|--------|-------------|
| `assistant` | `content` | Model text output |
| `tool_use` | `name`, `input` | Tool invocation |
| `tool_result` | `content`, `is_error` | Tool response |
| `result` | `cost_usd`, `session_id`, `turns` | Final summary |

---

## TypeScript SDK

### Installation

```bash
npm install @anthropic-ai/claude-agent-sdk
```

### Basic Usage

```typescript
import { query, ClaudeAgentOptions } from "@anthropic-ai/claude-agent-sdk";

const options: ClaudeAgentOptions = {
  permissionMode: "bypassPermissions",
  allowedTools: ["Read", "Edit", "Bash(npm test)"],
  model: "sonnet",
  cwd: "/path/to/project",
};

for await (const message of query("Implement auth module", options)) {
  if (message.type === "assistant") {
    console.log(message.content);
  }
}
```

### ClaudeAgentOptions (TypeScript)

| Field | Type | Description |
|-------|------|-------------|
| `permissionMode` | `string` | `"default"`, `"acceptEdits"`, `"bypassPermissions"`, `"dontAsk"` |
| `allowedTools` | `string[]` | Tools to pre-authorize |
| `disallowedTools` | `string[]` | Tools to block |
| `model` | `string` | Model name |
| `cwd` | `string` | Working directory |
| `maxTurns` | `number` | Maximum agentic turns |
| `maxBudgetUsd` | `number` | Spending cap |
| `systemPrompt` | `string` | Replace default system prompt |
| `appendSystemPrompt` | `string` | Append to default system prompt |
| `mcpConfig` | `string` | Path to MCP config file |
| `agents` | `object` | Subagent definitions |

### Multi-Turn Session (TypeScript)

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

let sessionId: string | undefined;

for await (const msg of query("Create user model", { model: "sonnet" })) {
  if (msg.type === "result") sessionId = msg.session_id;
}

for await (const msg of query("Add validation", {
  model: "sonnet",
  resume: sessionId,
})) {
  if (msg.type === "assistant") console.log(msg.content);
}
```

---

## SDK Permission Modes

| Mode | Python | TypeScript | Behavior |
|------|--------|------------|----------|
| Default | `"default"` | `"default"` | Prompt user (interactive) |
| Accept edits | `"acceptEdits"` | `"acceptEdits"` | Auto-approve edits, prompt bash |
| Bypass | `"bypassPermissions"` | `"bypassPermissions"` | Auto-approve all |
| Don't ask | N/A | `"dontAsk"` | TS-only: deny instead of prompt |

Best practice: always pair `bypassPermissions` with an `allowed_tools` whitelist and `disallowed_tools` blacklist. Never use bypass without restrictions outside a sandbox.
