---
description: Run incremental continual-learning — scan transcripts, extract durable facts, update AGENTS.md + CLAUDE.md + vault
---

# Continual Learning

Run the `g-continual-learning` skill now. Use the `agents-memory-updater` subagent for the full memory update flow.

Use incremental transcript processing with index file `.cursor/hooks/state/continual-learning-index.json`: only consider transcripts not in the index or transcripts whose mtime is newer than indexed mtime.

Have the subagent:
1. Refresh index mtimes for processed transcripts
2. Remove entries for deleted transcripts
3. Update `AGENTS.md` only for high-signal recurring user corrections and durable workspace facts
4. Mirror the same `## Learned Workspace Facts` section into `CLAUDE.md`
5. Write a vault note to `{vault}/projects/{project_name}/decisions/{date}_continual_learning.md`
6. Clean up `.galdr/logs/pending_reflection.json` if it exists

Exclude one-off/transient details and secrets.

If no meaningful updates exist, respond exactly: `No high-signal memory updates.`
