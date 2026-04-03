# Permissions & Hooks

Permission system, settings file configuration, and unattended execution patterns for Claude Code.

Official docs: https://docs.anthropic.com/en/docs/claude-code/permissions

---

## Permission Modes

| Mode | Behavior |
|------|----------|
| `plan` | Read-only, no edits, no commands |
| `acceptEdits` | Auto-approve file edits, prompt for bash |
| `askEdits` | Prompt for edits and bash |
| `askTools` | Prompt for all tool usage |
| `denyAll` | Deny all tool requests |
| `bypassPermissions` | Auto-approve everything (same as `--dangerously-skip-permissions`) |

---

## AllowedTools Pattern Syntax

```bash
--allowedTools "Read" "Edit" "Write"

# Bash with command patterns (glob matching)
--allowedTools "Bash(npm *)"          # npm commands only
--allowedTools "Bash(git *)"          # git commands only
--allowedTools "Bash(python -m *)"    # python module execution

# Deny patterns (prefix with !)
--allowedTools "Bash(!rm *)"          # block rm
--allowedTools "Bash(!sudo *)"        # block sudo
--allowedTools "Bash(!curl *)"        # block curl

# Combine multiple
--allowedTools "Read" "Edit" "Bash(npm *)" "Bash(git *)" "Bash(!rm *)"
```

---

## Settings File Configuration

### Project settings (committed)

```json
// .claude/settings.json
{
  "permissions": {
    "allow": ["Read", "Edit", "Bash(npm test)", "Bash(git *)"],
    "deny": ["Bash(rm *)", "Bash(sudo *)"]
  }
}
```

### Personal settings (gitignored)

```json
// .claude/settings.local.json
{
  "permissions": {
    "allow": ["Bash(docker *)"]
  }
}
```

---

## Unattended Agent Execution

For agents that must run without permission prompts:

```bash
claude -p "implement feature X" \
  --dangerously-skip-permissions \
  --allowedTools "Read" "Edit" "Write" "Bash(npm *)" "Bash(git *)" \
  --disallowedTools "Bash(rm -rf *)" "Bash(sudo *)" \
  --max-turns 50 \
  --max-budget-usd 5
```

Best practice: always pair `--dangerously-skip-permissions` with `--allowedTools` whitelist and `--disallowedTools` blacklist. Never use bypass without restrictions outside a sandbox.
