---
name: g-knowledge-refresh
description: Audit vault freshness, re-fetch expired sources, rebuild knowledge cards, prompt when topics age out. For refresh knowledge, stale notes, knowledge cards, research consolidation.
---

# galdr-knowledge-refresh

Maintain vault freshness by checking expiration dates, re-fetching sources, and consolidating knowledge cards.

## When to Use

- `@g-knowledge-refresh` — full freshness audit
- `@g-knowledge-refresh [topic]` — refresh a specific topic
- Automatically during `@g-cleanup` nightly maintenance
- When user says "refresh knowledge", "rebuild knowledge", "check stale"

## Freshness Audit

### Step 1: Read `_index.yaml`

Parse the vault index. For each note, check:

| Condition | Action |
|-----------|--------|
| `refresh_after` is set and past due | Queue for re-fetch |
| `expires_after` is set and past due | Flag as stale |
| `refresh_policy: daily` and last refresh > 24h | Queue for re-fetch |
| `refresh_policy: weekly` and last refresh > 7d | Queue for re-fetch |
| `refresh_policy: monthly` and last refresh > 30d | Queue for re-fetch |
| `source_volatility: high` and note > 14d old | Warn user |

### Step 2: Present Refresh Menu

```markdown
# Vault Freshness Report

## Stale Notes (expired)
| Note | Expired | Source | Action |
|------|---------|--------|--------|
| research/platforms/claude-code/api.md | 2026-03-01 | crawl4ai | Re-crawl recommended |

## Due for Refresh
| Note | Due | Policy | Source |
|------|-----|--------|--------|
| research/platforms/cursor/docs.md | 2026-03-25 | weekly | crawl4ai |

## High-Volatility Warnings
| Note | Age | Volatility | Suggestion |
|------|-----|------------|------------|
| research/articles/openai-codex.md | 21d | high | Consider refreshing |

## Knowledge Cards Due for Rebuild
| Card | Sources Changed | Last Built |
|------|-----------------|------------|
| knowledge/ai-agent-memory.md | 2 new sources | 2026-03-15 |
```

### Step 3: Wait for User Approval

- "refresh all stale" → re-fetch all expired/due notes
- "refresh platforms" → re-crawl platform docs only
- "rebuild [topic]" → rebuild a specific knowledge card
- "skip" → do nothing

### Step 4: Execute Refreshes

For each approved refresh:

1. **Platform doc sources**: Run `python scripts/platform_crawl.py --target {name}`
2. **URL sources**: Re-fetch with WebFetch, compare to existing content, update if changed
3. **Video sources**: Skip (videos don't change; `refresh_policy: none`)
4. **Knowledge cards**: Re-read all `source_notes`, re-synthesize, update card

After each refresh:
- Update `date` to today
- Set new `refresh_after` based on `refresh_policy`
- Reset `expires_after` based on content type
- Call `vault_sync` to update the database
- Run `vault-reindex.ps1` to update `_index.yaml`

## Building Knowledge Cards

### When to Build

- User asks to consolidate knowledge on a topic
- 3+ source notes share overlapping topics
- During freshness audit, source notes have changed since last card build

### How to Build

1. **Identify sources**: Search `_index.yaml` for notes matching the topic
2. **Read all sources**: Load the full content of each source note
3. **Synthesize**: Merge key points, deduplicate, organize by subtopic
4. **Write card**: Save to `{vault}/knowledge/{topic_slug}.md`
5. **Link back**: Include `source_notes` list in frontmatter and `[[wikilinks]]` in body

### Knowledge Card Frontmatter

```yaml
---
date: 2026-03-28
type: knowledge_card
ingestion_type: knowledge_card
title: "Topic: {Topic Name}"
topics: [{topic1}, {topic2}, ...]
source_notes:
  - research/videos/2026-03-27_source1.md
  - research/platforms/claude-code/source2.md
refresh_policy: on_demand
source_volatility: medium
expires_after: {date + 90 days}
last_rebuilt: 2026-03-28
---
```

### Knowledge Card Expiration

Knowledge cards have their own expiration independent of sources:

| Topic Domain | Default Expiry | Rationale |
|--------------|----------------|-----------|
| AI/ML tools & platforms | 90 days | Fast-moving field |
| Programming languages | 180 days | Moderate change rate |
| Mathematics/science | null (permanent) | Rarely invalidated |
| Business/legal | 365 days | Annual regulatory changes |
| Architecture patterns | 180 days | Evolves slowly |

## Integration with galdr-cleanup

Add to the nightly cleanup workflow after vault index regeneration:

```
### 10. Vault Freshness Check
1. Run freshness audit (Step 1-2 above)
2. If stale notes found, add to CLEANUP_REPORT.md under "Vault Freshness"
3. Do NOT auto-refresh — only flag for human review
```

## Vault Path Resolution

Source `vault-resolve.ps1` to get `$VaultPath`. All paths are relative to `$VaultPath`.
