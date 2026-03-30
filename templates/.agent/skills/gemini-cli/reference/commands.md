# Gemini CLI — Command Reference

Full reference for slash commands, input shortcuts, and keyboard shortcuts.

## Slash Commands

### Session Management

| Command | Description |
|---------|-------------|
| `/chat save <tag>` | Save conversation checkpoint with a named tag |
| `/chat resume <tag>` | Resume from a saved checkpoint |
| `/chat list` | List available checkpoint tags |
| `/chat delete <tag>` | Delete a saved checkpoint |
| `/chat share [file]` | Export conversation to .md or .json file |
| `/compress` | Replace chat context with a summary to save tokens |
| `/clear` | Clear terminal display (also `Ctrl+L`) |

Checkpoint storage: `~/.gemini/tmp/<project>/<tag>/`

### Tool & MCP Inspection

| Command | Description |
|---------|-------------|
| `/tools` | List available tools (names only) |
| `/tools desc` | List tools with full descriptions |
| `/tools nodesc` | List tools without descriptions |
| `/mcp` | List MCP servers and connection status |
| `/mcp desc` | Show MCP server and tool descriptions |
| `/mcp schema` | Show full JSON schema for MCP tool parameters |
| `/extensions` | List active extensions |

Toggle tool descriptions: `Ctrl+T`

### Memory (GEMINI.md)

| Command | Description |
|---------|-------------|
| `/memory show` | Display concatenated content from all GEMINI.md files |
| `/memory add <text>` | Add text to the model's instructional context |
| `/memory refresh` | Reload all GEMINI.md files from disk |
| `/memory list` | List paths of loaded GEMINI.md files |

### Configuration & UI

| Command | Description |
|---------|-------------|
| `/settings` | Open interactive settings editor |
| `/theme` | Change visual theme |
| `/editor` | Select preferred code editor |
| `/auth` | Change authentication method |
| `/vim` | Toggle vim keybinding mode |
| `/privacy` | View/set telemetry consent |

### Utility

| Command | Description |
|---------|-------------|
| `/help` or `/?` | Show all available commands |
| `/about` | Show version and system info |
| `/stats` | Show token usage, cached tokens, session duration |
| `/copy` | Copy last model output to clipboard |
| `/bug [title]` | File a GitHub issue (title becomes headline) |
| `/restore [id]` | Restore files to pre-tool-call state (requires `--checkpointing`) |
| `/init` | Generate a GEMINI.md for the current project |
| `/quit` or `/exit` | Exit the CLI |

### Custom Commands

User-defined commands via TOML files:
- User-level: `~/.gemini/commands/*.toml`
- Project-level: `.gemini/commands/*.toml`
- Extension-provided: `.gemini/extensions/<name>/commands/*.toml`

Nested directories create namespaced commands (e.g., `commands/gcs/sync.toml` → `/gcs:sync`).

## Input Shortcuts

| Syntax | Description |
|--------|-------------|
| `@path/to/file.txt` | Inject file content into the prompt |
| `@path/to/dir/` | Inject directory contents (respects .gitignore) |
| `!ls -la` | Execute shell command and return to CLI |
| `!` (alone) | Toggle persistent shell mode |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+L` | Clear terminal |
| `Ctrl+T` | Toggle tool descriptions |
| `Ctrl+Z` | Undo in input prompt |
| `Ctrl+Shift+Z` | Redo in input prompt |
| `Ctrl+C` | Cancel current operation |
| `Escape` | Return to normal mode (vim mode) |
