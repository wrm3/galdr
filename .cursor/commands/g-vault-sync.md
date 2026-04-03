# Command: @g-vault-sync

## Purpose
Bulk sync all local vault `.md` files to the PostgreSQL database with pgvector embeddings.

## Usage
```
@g-vault-sync
```

Or specify a subfolder:
```
@g-vault-sync videos/summaries/
@g-vault-sync research/
```

## How It Works

### Step 1: Resolve Vault Path
Reads `GALDR_KNOWLEDGE_WELL_PATH` from `.env` to find the vault root.

### Step 2: Sync Files
Calls `vault_sync` MCP tool with `mode="full"` to:
- Scan all `.md` files in the vault
- Parse YAML frontmatter and extract metadata
- Generate OpenAI embeddings for each note's content
- Upsert into the `vault_notes` PostgreSQL table
- Remove DB entries for files that no longer exist locally

### Step 3: Report Results
Shows counts of created, updated, unchanged, and removed notes.

## When to Use

- After manually adding files to the vault folder
- After a migration or vault restructure
- When `@g-vault-search` results seem stale or incomplete
- First-time setup of the vault database

## Related Commands

| Command | When to Use |
|---------|-------------|
| `@g-vault-search` | Search after syncing |
| `@g-vault-store` | Write + sync a single note |
