# Gemini CLI — Extensions

Extensions package prompts, MCP servers, and custom commands into installable, shareable units.

## Extension Management Commands

| Command | Description |
|---------|-------------|
| `gemini extensions install <url\|path>` | Install from GitHub URL or local path |
| `gemini extensions uninstall <name>` | Remove an extension |
| `gemini extensions update <name>` | Update a specific extension |
| `gemini extensions update --all` | Update all extensions |
| `gemini extensions enable <name> [--scope=workspace]` | Enable an extension |
| `gemini extensions disable <name> [--scope=workspace]` | Disable an extension |
| `gemini extensions list` | List installed extensions (outside CLI) |
| `/extensions` | List active extensions (inside CLI) |

## Extension Development

### Create from Template

```bash
gemini extensions new path/to/my-ext custom-commands
```

Available templates: `context`, `custom-commands`, `exclude-tools`, `mcp-server`.

### Link for Development

```bash
gemini extensions link path/to/my-ext
```

Creates a symlink so changes are reflected without running `update`.

## Extension Structure

```
~/.gemini/extensions/my-extension/
├── gemini-extension.json    # Required: extension manifest
├── GEMINI.md                # Optional: context injected into model
├── commands/                # Optional: custom TOML commands
│   ├── deploy.toml
│   └── gcs/
│       └── sync.toml        # Becomes /gcs:sync
└── my-server.js             # Optional: MCP server script
```

### gemini-extension.json

```json
{
  "name": "my-extension",
  "version": "1.0.0",
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["${extensionPath}${/}my-server.js"]
    }
  },
  "contextFileName": "GEMINI.md",
  "excludeTools": ["run_shell_command(rm -rf)"]
}
```

### Variable Substitution

| Variable | Description |
|----------|-------------|
| `${extensionPath}` | Fully-qualified path to the extension directory |
| `${workspacePath}` | Fully-qualified path to the current workspace |
| `${/}` or `${pathSeparator}` | OS-specific path separator |

## Conflict Resolution

Extension commands have lowest precedence:
1. User/project command wins → extension command renamed to `/<ext-name>.command`
2. No conflict → extension command uses its natural name

## Releasing Extensions

Extensions can be published via GitHub releases. See the official
[Extension Releasing](https://google-gemini.github.io/gemini-cli/docs/extensions/extension-releasing.html) docs.
