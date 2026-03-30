# Command: @g-vault-store

## Purpose
Write a note to the vault and sync it to the database for semantic search.

## Usage
```
@g-vault-store
```

Then describe what to store:
```
@g-vault-store decision: we chose PostgreSQL over SQLite for the vault backend
@g-vault-store correction: Docker bind mounts are unreliable on Windows non-C drives
@g-vault-store research: summary of MCP protocol changes in 2026
```

## How It Works

### Step 1: Determine Note Type and Path
Based on your description, the agent selects the appropriate note type and vault path:
- `decision` → `projects/{pid}_{name}/decisions/`
- `correction` → `knowledge/corrections/`
- `research` → `research/topics/`
- `preference` → `knowledge/preferences/`
- `session` → `projects/{pid}_{name}/sessions/`

### Step 2: Write the File
Creates a `.md` file with proper YAML frontmatter (date, project_id, source, type, tags) and body content.

### Step 3: Sync to Database
Calls `vault_sync` MCP tool to index the note in PostgreSQL with embeddings, making it searchable via `@g-vault-search` and the web UI.

### Step 4: Dual-Write (if applicable)
For research, harvests, and analyses, writes to both project-specific and global vault locations.

## Related Commands

| Command | When to Use |
|---------|-------------|
| `@g-vault-search` | Find existing notes |
| `@g-vault-sync` | Bulk sync if many files were written manually |
| `@g-harvest` | Analyze external source and store harvest results |
