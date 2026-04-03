# Command: @g-vault-research

## Purpose
Research a topic using available tools (web search, MCP research, video analysis), then write the results to the vault and sync to the database.

## Usage
```
@g-vault-research
```

Then describe what to research:
```
@g-vault-research MCP protocol changes in 2026
@g-vault-research analyze this video: https://youtu.be/abc123
@g-vault-research compare Cursor vs Claude Code agent capabilities
```

## How It Works

### Step 1: Research
Uses the appropriate tools based on the source:
- **Web topics**: `WebSearch`, `research_deep` MCP tool
- **YouTube videos**: `video_analyze` MCP tool
- **Articles/URLs**: `WebFetch`, content extraction

### Step 2: Format Results
Structures the research as a vault note with proper frontmatter, summary, key findings, and source attribution.

### Step 3: Write to Vault
Writes the `.md` file to the appropriate vault location:
- Video analysis → `videos/summaries/` + `projects/{pid}/videos/`
- Web research → `research/topics/` + `projects/{pid}/research/`
- Platform docs → `research/platforms/`

### Step 4: Sync to Database
Calls `vault_sync` to index the note with embeddings for future semantic search.

## Related Commands

| Command | When to Use |
|---------|-------------|
| `@g-vault-search` | Find previous research |
| `@g-vault-store` | Store a note without research |
| `@g-harvest` | Analyze external source for actionable improvements |
