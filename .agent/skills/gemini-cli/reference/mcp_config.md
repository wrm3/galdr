# Gemini CLI — MCP Server Configuration

How to add and configure MCP (Model Context Protocol) servers in Gemini CLI.

## Configuration Location

MCP servers are defined in `settings.json` files:
- User-level: `~/.gemini/settings.json`
- Project-level: `.gemini/settings.json`
- Extension-provided: via `gemini-extension.json`

Project settings override user settings. Extension MCP servers have lowest precedence.

## Server Definition Format

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@my/mcp-server"],
      "cwd": "/path/to/working/dir",
      "env": {
        "API_KEY": "$MY_API_KEY",
        "DB_URL": "${DATABASE_URL}"
      },
      "timeout": 30000,
      "trust": true
    }
  }
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `command` | string | Executable to launch the MCP server |
| `args` | string[] | Arguments passed to the command |
| `cwd` | string | Working directory for the server process |
| `env` | object | Environment variables (supports `$VAR` and `${VAR}` substitution) |
| `timeout` | number | Startup timeout in milliseconds |
| `trust` | boolean | Skip tool confirmation for this server's tools (not available in extensions) |

## Inspecting MCP Servers

```
/mcp              # List servers and connection status
/mcp desc         # Show tool descriptions
/mcp schema       # Show full JSON parameter schemas
Ctrl+T            # Toggle description visibility
```

## Example: galdr MCP Server

```json
{
  "mcpServers": {
    "galdr": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://localhost:8082/mcp/sse"],
      "env": {},
      "timeout": 60000
    }
  }
}
```

## Sandbox Considerations

When running with `--sandbox`, MCP server executables must be available inside the sandbox container. Install required tools in your custom `sandbox.Dockerfile` or use servers that communicate over network protocols.
