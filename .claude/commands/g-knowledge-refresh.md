# @g-knowledge-refresh — Vault Freshness & Knowledge Rebuild

**Purpose**: Audit vault notes for staleness, re-fetch expired sources, and rebuild knowledge cards from updated sources. Prompts user before making changes.

**Safe to run**: Yes — read-only audit by default. Writes only after user approval.

---

## Usage

- `@g-knowledge-refresh` — Full freshness audit of all vault notes
- `@g-knowledge-refresh [topic]` — Refresh/rebuild a specific topic
- `@g-knowledge-refresh --stale-only` — Show only expired/overdue notes
- `@g-knowledge-refresh --rebuild [topic]` — Rebuild a knowledge card

---

## What It Does

1. **Reads `_index.yaml`** from the vault root
2. **Checks each note** against its `refresh_after`, `expires_after`, and `refresh_policy` fields
3. **Presents a freshness report** showing stale, due-for-refresh, and high-volatility notes
4. **Waits for user approval** before re-fetching or rebuilding anything
5. **Executes approved refreshes** (re-crawl, re-fetch, rebuild knowledge cards)
6. **Updates `_index.yaml`** after all changes

See the `g-knowledge-refresh` skill for full implementation details.

---

## Integration

- Called automatically by `@g-cleanup` during nightly maintenance (audit only, no auto-refresh)
- Can be run manually at any time
- Knowledge cards are rebuilt on demand or when source notes change
