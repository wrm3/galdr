---
name: g-harvest
description: Analyze external sources and present selective improvement ideas. User approves what to adopt — nothing changes without approval.
---
# g-harvest

Analyze external sources and present improvement opportunities as a curated menu. The user selects what they want — only approved items become tasks. **Nothing changes without explicit user approval.**

## When to Use

Trigger: `@g-harvest [URL or path]`

Use when the user wants to:
- Review an external repo for ideas (NOT merge it into our project)
- Analyze an article, video transcript, or research for applicable improvements
- Browse what a library/framework offers and pick specific features
- Evaluate a competing product for ideas worth adopting

**Trigger phrases**: "harvest", "what can we learn from", "analyze this for ideas", "what's useful in", "review this for improvements", "cherry-pick from", "what should we adopt from"

## When NOT to Use

| Aspect | Harvest (this skill) | Integration (`@g-analyze-codebase`) |
|--------|---------------------|----------------------------------------|
| **Source** | External source you don't own | Your own projects being merged |
| **Goal** | Selectively adopt ideas | Full deep merge |
| **User role** | Active chooser at every step | Approves overall plan |
| **Default** | Nothing adopted unless approved | Everything mapped for integration |
| **Risk** | Low — controlled, incremental | High — architectural restructuring |
| **Output** | Menu of suggestions → user picks | Complete integration phase |

Also NOT for: simple code reviews (`g-code-reviewer`), bug tracking (`g-qa`).

---

## Steps

### Step 1: Fetch & Understand the Source

Adapt to source type:

- **URL** → WebFetch or RAG search
- **GitHub repo** → explore README, key source files, architecture
- **Article/blog** → extract key points
- **Video** → use youtube-video-analysis skill

**Source-specific checklists:**

**Repository**: Tech stack identified · Entry points mapped · Major subsystems listed · Novel patterns noted · Config/security approach documented · Dependencies of interest noted

**Article/Document**: Key thesis extracted · Actionable techniques identified · Referenced tools/libraries noted · Applicability assessed · Counter-arguments noted

**Video/Transcript**: Key demonstrations captured · Tools/techniques shown · Code patterns discussed · Timestamps for important sections noted

**Research/Paper**: Findings summarized · Applicable techniques identified · Implementations referenced · Potential improvements to our system noted

### Step 2: Map the Source

Read before judging:
- What does it do?
- Key features/patterns/approaches
- Tech stack and architecture highlights
- Anything notably clever or novel?

### Step 3: Compare to Current Project

- What do we already have? (no point adopting duplicates)
- What gaps does this fill?
- What patterns are better than ours?
- What would be over-engineering for our scale?

### Step 4: Present the Harvest Menu

This is the critical step that prevents scope creep. Present findings as a numbered menu:

```markdown
## Harvest Menu: [Source Name]

### Category: {e.g., "AI Agent Capabilities"}

**H-01: {Short descriptive title}**
- **What it is**: {2-3 sentences}
- **Where in source**: {file path, section, or timestamp}
- **How it helps us**: {1-2 sentences on benefit to OUR project}
- **Effort**: Small (< 4h) | Medium (1-2 days) | Large (3+ days)
- **Affects subsystems**: {which of our subsystems would change}
- **Risk**: Low | Medium | High — {brief reason}

---

### Summary

| # | Suggestion | Effort | Risk | Category |
|---|-----------|--------|------|----------|
| H-01 | {title} | Small | Low | {cat} |

**Total suggestions**: {count}
**Quick wins (Small + Low risk)**: {count}

**Your turn.** Reply with:
- Numbers you want (e.g., "H-01, H-03, H-07")
- "tell me more about H-05" for details
- "none" to pass
```

**Menu rules:**
1. Maximum 15–20 suggestions — if more, split into "top picks" and "also available"
2. Order by impact — most valuable first
3. Be honest about effort — don't underestimate
4. Flag conflicts with our architecture
5. Suggest groupings — "H-01 and H-03 work well together"
6. Mark items that overlap with existing planned work in TASKS.md
7. Default is "take nothing" — never assume "take all"

### Step 5: User Selection & Discussion

**Wait for the user to respond.** They will select items, ask questions, modify suggestions, reject items, or request alternatives.

During discussion:
- Stay focused on the user's selections
- Don't re-pitch rejected items
- If user says "yes to all" — confirm: "That's {X} tasks across {Y} subsystems. Want me to proceed, or review the Large/High-risk ones first?"
- Keep a running tally of what's approved

### Step 6: Create Tasks (Approved Items Only)

For each adopted item, use galdr-task-new skill to create a task:
- Include `[Harvest: {source_name}]` in the task title
- Reference the harvest item (H-XX) and source URL in task notes
- Ask the user which phase if unclear

### Step 7: Write Harvest Results to Vault

Always write results, even if nothing was adopted.

Read `.galdr/.project_id` for the project UUID. Resolve vault path from `.galdr/.vault_location` (fallback: `.galdr/vault/`).

**Path**: `{vault}/research/harvests/{date}_{source-name}.md`

```yaml
---
date: YYYY-MM-DD
project: {project_name}
project_id: {from .galdr/.project_id}
source: cursor/agent
type: harvest
ingestion_type: harvest
source_type: github | article | video | paper
url: {source URL}
topics: [harvest, {topic tags}]
---

# Harvest: {Source Name}

## Source
- **URL**: {url}
- **Type**: {github | article | video | paper}
- **Analyzed for project**: [[{project_name}]]

## Adopted Items
- Item N: {description} → Task #{id}

## Skipped Items
- {what was not adopted and why}

## Key Patterns Discovered
- {reusable patterns worth remembering across projects}
```

---

## Anti-Patterns

**DO NOT:**
- Create tasks before user approves suggestions
- Assume the user wants everything
- Start modifying code during analysis
- Treat the source as authoritative over our architecture
- Create a full integration phase without user selection
- Suggest replacing existing working subsystems
- Scope-creep from "harvest ideas" into "rebuild around this"

---

*This skill ensures external sources enrich our project without hijacking it. The user is always in control.*
