# Command: @g-vault-search

## Purpose
Search the vault knowledge base using semantic (vector) search via the database, with fallback to local file grep.

## Usage
```
@g-vault-search
```

Then provide your query:
```
@g-vault-search docker bind mount issues
@g-vault-search what videos have we analyzed about AI agents?
@g-vault-search type:harvest crawl4ai
```

## How It Works

### Step 1: Database Semantic Search
Calls the `vault_search` MCP tool with your query. This uses pgvector embeddings for meaning-based matching against all synced vault notes.

### Step 2: Fallback to Local Files
If the database has no results (or is unavailable), falls back to searching local vault files using Grep/ripgrep.

### Step 3: Present Results
Returns matching notes with title, path, snippet, similarity score, and tags. You can then ask to read any result in full.

## Filters

| Filter | Example | Description |
|--------|---------|-------------|
| `type:` | `type:video_summary` | Filter by note type |
| `project:` | `project:galdr` | Filter by project |
| `tags:` | `tags:docker,platform` | Filter by tags |

## Related Commands

| Command | When to Use |
|---------|-------------|
| `@g-vault-store` | Write a new note to the vault |
| `@g-vault-sync` | Sync local files to DB if search results seem stale |
| `@g-vault-research` | Research a topic and store results |
