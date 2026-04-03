# Gemini CLI — Built-in Tools

Reference for all built-in tools available to the Gemini model.

## Tool Inventory

| Tool | Description |
|------|-------------|
| `read_file` | Read contents of a single file |
| `write_file` | Create or overwrite a file |
| `edit` | Make targeted edits to existing files |
| `read_many_files` | Read content from multiple files or entire directories (git-aware filtering) |
| `run_shell_command` | Execute shell commands (bash on Linux/macOS, cmd.exe on Windows) |
| `web_fetch` | Retrieve content from a URL |
| `google_web_search` | Search the web via Google |
| `save_memory` | Persist information to GEMINI.md for future sessions |

## Tool Permissions

Tools that modify the filesystem or execute commands require user confirmation by default.

### Auto-Approve Specific Tools

In `.gemini/settings.json`:

```json
{
  "tools": {
    "allowed": [
      "run_shell_command(git)",
      "run_shell_command(npm test)",
      "read_file",
      "read_many_files"
    ]
  }
}
```

Prefix matching: `run_shell_command(git)` approves `git status`, `git commit`, etc.

### Restrict Available Tools

```json
{
  "tools": {
    "core": ["read_file", "read_many_files", "google_web_search"],
    "exclude": ["run_shell_command"]
  }
}
```

### YOLO Mode

```bash
gemini --yolo
```

Auto-approves all tool calls. Use only in sandboxed or disposable environments.

## Sandbox Mode

Run tools in an isolated Docker container:

```bash
gemini --sandbox
gemini --sandbox -y -p "refactor src/"
```

Sandbox restrictions:
- File writes scoped to project directory
- Network access may be limited
- MCP servers must be available inside the container
- Custom sandbox profiles: `.gemini/sandbox.Dockerfile` or `.gemini/sandbox-macos-custom.sb`

## Shell Tool Details

- Linux/macOS: executes via `bash`
- Windows: executes via `cmd.exe`
- Sets `GEMINI_CLI=1` env var in subprocess
- Interactive shell mode available: `tools.shell.enableInteractiveShell: true`
- Output summarization: configure `model.summarizeToolOutput` for long outputs

## Memory Tool

`save_memory` writes to `~/.gemini/GEMINI.md` (user-level) for cross-session persistence.

Use `/memory show` to inspect and `/memory refresh` to reload from disk.
