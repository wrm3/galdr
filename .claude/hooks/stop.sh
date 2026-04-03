#!/bin/bash
# Claude Code Stop Hook — galdr memory ingestion
#
# Triggered by Claude Code when a session ends (stop event).
# Runs claude_adapter.py to ingest the session into galdr's memory system.
#
# Environment variables provided by Claude Code:
#   CLAUDE_SESSION_ID   - UUID of the completed session
#   CLAUDE_PROJECT_DIR  - Project working directory (may not be set in all versions)
#
# Hook input (stdin JSON):
#   {"session_id": "...", "transcript_path": "..."}
#
# Installation:
#   Add to ~/.claude/settings.json or project .claude/settings.json:
#   {
#     "hooks": {
#       "Stop": [{"matcher": "", "hooks": [{"type": "command", "command": "/path/to/stop.sh"}]}]
#     }
#   }

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/../logs"
mkdir -p "$LOG_DIR"
DATE_PREFIX=$(date +"%Y-%m-%d")
LOG_FILE="$LOG_DIR/${DATE_PREFIX}_claude_memory.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "[$TIMESTAMP] [STOP HOOK] Starting memory capture" >> "$LOG_FILE"

# Read stdin JSON (Claude Code passes hook data via stdin)
HOOK_INPUT=""
if [ -t 0 ]; then
    HOOK_INPUT="{}"
else
    HOOK_INPUT=$(cat)
fi

# Extract session_id from stdin JSON (fallback to env var)
SESSION_ID="${CLAUDE_SESSION_ID:-}"
if [ -z "$SESSION_ID" ] && command -v python3 &>/dev/null; then
    SESSION_ID=$(echo "$HOOK_INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('session_id',''))" 2>/dev/null || echo "")
fi

if [ -z "$SESSION_ID" ]; then
    echo "[$TIMESTAMP] [STOP HOOK] No session_id — skipping" >> "$LOG_FILE"
    exit 0
fi

# Project path — prefer CLAUDE_PROJECT_DIR, fallback to CWD
PROJECT_PATH="${CLAUDE_PROJECT_DIR:-$(pwd)}"

echo "[$TIMESTAMP] [STOP HOOK] session=$SESSION_ID project=$PROJECT_PATH" >> "$LOG_FILE"

# Locate claude_adapter.py — search relative to this script and in hooks dir
ADAPTER=""
for candidate in \
    "$SCRIPT_DIR/claude_adapter.py" \
    "$SCRIPT_DIR/../hooks/claude_adapter.py" \
    "$PROJECT_PATH/.cursor/hooks/claude_adapter.py" \
    "$PROJECT_PATH/.claude/hooks/claude_adapter.py"
do
    if [ -f "$candidate" ]; then
        ADAPTER="$candidate"
        break
    fi
done

if [ -z "$ADAPTER" ]; then
    echo "[$TIMESTAMP] [STOP HOOK] claude_adapter.py not found — skipping" >> "$LOG_FILE"
    exit 0
fi

# Find python
PYTHON_CMD=""
for py in python3 python; do
    if command -v "$py" &>/dev/null; then
        PYTHON_CMD="$py"
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "[$TIMESTAMP] [STOP HOOK] Python not found — skipping" >> "$LOG_FILE"
    exit 0
fi

# Run adapter in background so hook returns immediately
"$PYTHON_CMD" "$ADAPTER" \
    --session-id "$SESSION_ID" \
    --project-path "$PROJECT_PATH" \
    --status completed \
    >> "$LOG_FILE" 2>&1 &

echo "[$TIMESTAMP] [STOP HOOK] Adapter launched (background pid=$!)" >> "$LOG_FILE"

# Exit 0 — always let Claude Code proceed regardless of adapter status
exit 0
