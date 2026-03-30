---
name: g-codebase-analysis
description: Deep merge of codebases you own—architecture map, vault, galdr tasks. For external ideas only, use g-harvest, not full integration.
---

# galdr-codebase-analysis

Systematically merge two or more of your own projects by mapping their architectures, comparing components, identifying overlaps, and producing a structured integration plan. **This skill is for deep merges of projects you own -- not for browsing external sources for ideas.**

## Critical Distinction: Integration vs. Harvest

| Aspect | Integration (THIS skill) | Harvest (`@g-harvest`) |
|--------|-------------------------|---------------------------|
| **Source** | YOUR OWN projects being merged | External source you don't own |
| **Goal** | Deep structural merge | Selectively adopt ideas |
| **Default** | Map everything for integration | Adopt nothing unless approved |
| **User role** | Approve overall plan | Active chooser at every step |
| **Risk** | High -- architectural restructuring | Low -- controlled, incremental |
| **Scope** | Comprehensive feature parity | Only what user picks |

**If the user says "analyze", "review", or "what can we learn from" an external source, use `@g-harvest` instead.**
**Only use THIS skill when the user explicitly wants to MERGE or COMBINE two of their own projects.**

## When to Use This Skill

Use this skill when the user requests:
- **Merging two of their own projects together**
- Combining separate codebases they own into one
- Deep structural integration of their own systems
- Full feature parity analysis between their own projects
- Planning a migration from one of their systems to another

**Trigger phrases**: "merge these projects", "combine these codebases", "integrate my projects", "absorb this into", "full integration", "feature parity between my projects"

## When NOT to Use This Skill

DO NOT use this skill for:
- **Analyzing external repos for ideas** → Use `@g-harvest` (g-harvest skill)
- **Reviewing a library/framework for selective adoption** → Use `@g-harvest`
- **Browsing what a project offers** → Use `@g-harvest`
- Simple code reviews → Use `g-code-reviewer` skill
- Planning features from scratch → Use `g-planning` skill
- Bug tracking → Use `g-qa` skill


## Safeguards (MANDATORY)

### Before Starting:
1. **Confirm intent**: "You want to do a full deep merge of {Project A} into {Project B}. This will create a comprehensive integration phase with potentially 40-60+ tasks. Is that what you want, or would `@g-harvest` (selective adoption) be more appropriate?"
2. **Load SUBSYSTEMS.md**: Understand current architecture before proposing changes
3. **Identify what's working**: Never propose replacing working subsystems without explicit justification

### During Analysis:
4. **Preserve existing architecture**: Our project's architecture is the foundation. The merged project adapts to us, not the other way around.
5. **Flag conflicts immediately**: If the merge would disconnect, break, or replace existing working systems, STOP and inform the user
6. **Never touch systems outside scope**: Other Docker stacks, other repos, other projects are OFF LIMITS

### Before Creating Tasks:
7. **Present the integration plan for approval BEFORE creating tasks**: Show the proposed phase, task categories, and estimated scope. Wait for user approval.
8. **Maximum task batch**: If the plan exceeds 30 tasks, present in batches and get approval per batch
9. **Update SUBSYSTEMS.md**: Every integration plan must include SUBSYSTEMS.md updates as part of the deliverables

---

## 5-Phase Analysis Process

### Phase 1: Codebase Exploration

**Goal:** Build a complete mental model of the external project's architecture.

**Steps:**

1. **Locate the codebase** — Confirm the path (usually in `research/` or a specified directory)

2. **Top-level structure scan** — Use `LS` on the root to understand project layout:
   ```
   LS target_directory: {codebase_path}
   ```

3. **Entry point identification** — Find `package.json`, `setup.py`, `Cargo.toml`, `go.mod`, `Makefile`, or equivalent to understand:
   - Language/runtime
   - Dependencies
   - Build scripts
   - Entry points

4. **Parallel deep-dive exploration** — Launch 3-4 `Task` subagents (type: `explore`) simultaneously, each assigned a major section of the codebase:
   - Agent 1: Core business logic / main systems
   - Agent 2: Infrastructure, config, auth, networking
   - Agent 3: UI, CLI, commands, user-facing interfaces
   - Agent 4: Extensions, plugins, integrations

   Each agent should report:
   - What each directory/module does (2-3 sentences)
   - Key files and their purposes
   - Key exports/classes/functions
   - How it relates to other modules
   - Configuration/settings it uses

5. **Settings and config audit** — Search for all configuration:
   ```
   Grep pattern: "process\.env\.|os\.environ|config\.|settings\." in the codebase
   Glob pattern: "**/.env*", "**/config.*", "**/settings.*"
   ```

**Output:** Raw exploration data from all agents.

---

### Phase 2: Architecture Document

**Goal:** Produce a structured architecture mapping document.

**Document Template:** `docs/YYYYMMDD_HHMMSS_Cursor_{PROJECT}_ARCHITECTURE_MAP.md`

**Required Sections:**

```markdown
# {Project Name} Architecture Map

> Complete component mapping of {project} codebase
> Source: {path}
> Generated: {date}

---

## Table of Contents
{Auto-generated from sections}

## 1. Overview
- What the project does (3-5 sentences)
- Tech stack (language, runtime, frameworks)
- Entry point flow diagram
- Default ports/URLs
- Data directories

## 2-N. Component Sections (one per major subsystem)
For each component:

### {N}. {Component Name}
**Location:** `{relative_path}/`
**Purpose:** {2-3 sentences}

#### Key Files
| File | Purpose |
|------|---------|
| `file.ts` | What it does |

#### How It Works
{3-5 sentence explanation of the flow}

#### Configuration
| Setting | Default | Purpose |
|---------|---------|---------|
| `SETTING_NAME` | `value` | What it controls |

## Architecture Diagram
{ASCII or Mermaid diagram showing component relationships}

## Settings/Config Reference
{Complete table of ALL settings, env vars, config options}
```

---

### Phase 3: Comparison Document

**Goal:** Map every external component to our equivalent (or lack thereof).

**Document Template:** `docs/YYYYMMDD_HHMMSS_Cursor_{PROJECT}_VS_GALDRWORKS_COMPARISON.md`

**Required Sections:**

```markdown
# {Project} vs GaldrWorks Component Comparison

## Comparison Legend
| Symbol | Meaning |
|--------|---------|
| ✅ TW | GaldrWorks has equivalent or better |
| ⚠️ Partial | GaldrWorks has partial implementation |
| ❌ Missing | GaldrWorks lacks this entirely |
| 🔄 Different | Different approach, not directly comparable |
| ⭐ TW Better | GaldrWorks version is superior |
| ⭐ {Project} Better | External version is superior |

## Component Comparison Tables (one per subsystem)
| Component | {Project} | GaldrWorks | Winner | TW Location |
|-----------|-----------|------------|--------|-------------|

## Unique GaldrWorks Features (No {Project} Equivalent)
{What we have that they don't}

## Priority Integration Gaps
| Priority | Component | Impact | Effort |
|----------|-----------|--------|--------|
| 🔴 HIGH | ... | ... | ... |
| 🟡 MEDIUM | ... | ... | ... |
| 🟢 LOW | ... | ... | ... |
| ⚪ SKIP | ... | reason | ... |

## Settings/Config Comparison
| {Project} Setting | Purpose | GaldrWorks Status | Action Needed |
|-------------------|---------|-------------------|---------------|
```

**Comparison Guidelines:**
- Be honest about which is better — don't bias toward our system
- "Different approach" is valid — not everything maps 1:1
- Mark items as SKIP if we intentionally don't need them
- Include effort estimates (Low/Medium/High) for missing items
- Reference exact file paths in GaldrWorks for existing implementations

---

### Phase 4: Integration Plan (Phase + Tasks)

**Goal:** Create a new galdr Phase with fully specced tasks.

**🚨 MANDATORY: Present plan for approval BEFORE creating ANY tasks.**

```markdown
## 📋 Proposed Integration Plan

**Merging**: {Project A} into {Project B}
**Proposed Phase**: Phase {N} - {Name}
**Estimated Tasks**: {count} tasks across {count} categories
**Estimated Total Effort**: {range}

### Task Categories:
1. {Category 1}: {count} tasks ({brief description})
2. {Category 2}: {count} tasks ({brief description})
...

### Subsystems Affected:
- {subsystem 1}: {what changes}
- {subsystem 2}: {what changes}

### Risks:
- {risk 1}
- {risk 2}

**Approve this plan?** (yes / modify / reduce scope / cancel)
```

**Wait for user approval before proceeding. If user says "modify" or "reduce scope", adjust and re-present.**

**Steps (after approval):**

1. **Determine next phase number** — Read `.galdr/TASKS.md`, find highest phase number, use N+1

2. **Create phase file** — `.galdr/phases/phase{N}_{kebab-name}.md` with proper YAML frontmatter:
   ```yaml
   ---
   phase: {N}
   name: '{Project Name} Full Integration & Verification'
   status: planning
   subsystems: [{affected_subsystems}]
   task_range: '{N*100}-{N*100+99}'
   prerequisites: [{prior_phases}]
   ---
   ```

3. **Generate task list** — Organize tasks into logical categories:

   **Task Categories (use as applicable):**
   - **Integration Verification** — Verify existing integrations work
   - **Missing Capability Implementation** — Build what's missing
   - **Settings & Configuration** — Surface all configs in our UI
   - **Protocol/Communication** — API and messaging integration
   - **Security & Auth** — Security feature parity
   - **UI/Dashboard** — Management interfaces
   - **Testing & Documentation** — Verification and docs

   **Task Sizing Guidelines:**
   - Each task should be completable in 1-4 hours
   - Complex components should be split into sub-tasks
   - Include verification tasks for existing integrations
   - Include a final "feature parity checklist" task
   - Include a "phase completion documentation" task

4. **Add to TASKS.md** — Insert phase header and all tasks (with `[ ]` status)

5. **Update summary statistics** — Update the stats table at bottom of TASKS.md

**Task Naming Convention:**
```
Task {ID}: {Action verb} {component} - {brief description} [{PRIORITY}]
```

**Priority Levels:**
- `[CRITICAL]` — System doesn't work without this
- `[HIGH]` — Important for feature parity
- `[MEDIUM]` — Nice to have, improves system
- `[LOW]` — Can defer, minimal impact

---

### Phase 4b: Write Analysis to Vault

**Goal:** Persist the analysis to the galdr vault so the project (and other projects) can reference it later.

Read `.galdr/.project_id` to get the project UUID. Resolve the vault path (check `.env` for `GALDR_KNOWLEDGE_WELL_PATH`, else use `.galdr/vault/`).

Write to **two locations** (dual-write pattern):

**Project copy**: `{vault}/projects/{project_id}_{project_name}/research/analyses/{date}_{target-project}.md`
**Global copy**: `{vault}/research/analyses/{date}_{target-project}.md`

Both files use this template:
```yaml
---
date: YYYY-MM-DD
project: {project_name}
project_id: {from .galdr/.project_id}
source: cursor/agent
type: codebase-analysis
source_type: github | repo-local
source_repo: {URL or local path}
tags: [integration, architecture, analysis, {target-project}]
---

# Codebase Analysis: {Target Project}

## Source
- **Path/URL**: {path or GitHub URL}
- **Analyzed for integration into**: [[{project_name}]]

## Architecture Summary
{key findings from Phase 1-2 — tech stack, major components, architecture highlights}

## Comparison Highlights
{key findings from Phase 3 — what we have vs what they have, winners}

## Integration Plan Summary
- Phase {N}: {name}
- {X} tasks created (IDs {range})
- Key subsystems affected: {list}

## Reusable Patterns
{patterns from the analyzed codebase that could benefit other projects}

## Documents Generated
- Architecture map: [[{architecture_doc_name}]]
- Comparison: [[{comparison_doc_name}]]
```

The global copy allows other projects to discover this analysis. If the source is a GitHub repo, include the `source_repo` URL so it's searchable.

---

### Phase 5: Deliverables Verification

**Goal:** Confirm all outputs are complete and consistent.

**Checklist:**
- [ ] **User approved the integration plan** before tasks were created
- [ ] Architecture document created in `docs/`
- [ ] Comparison document created in `docs/`
- [ ] **Vault analysis note written** (both project and global copies)
- [ ] Phase file created in `.galdr/phases/`
- [ ] All tasks added to `.galdr/TASKS.md`
- [ ] Summary statistics updated in TASKS.md
- [ ] Phase file and TASKS.md header are in sync
- [ ] Task IDs are in correct range for the phase
- [ ] No task references non-existent components
- [ ] Settings audit is complete
- [ ] All documents follow naming convention
- [ ] **SUBSYSTEMS.md updated** with any new/changed/deprecated subsystems
- [ ] **No existing working systems were disconnected or replaced** without explicit justification
- [ ] **No systems outside this project were touched** (other Docker stacks, other repos)

---

## Parallel Exploration Strategy

For maximum efficiency, launch exploration agents in parallel:

```
Agent 1 (explore): Core systems + business logic
Agent 2 (explore): Infrastructure + config + auth + networking
Agent 3 (explore): UI + CLI + commands + user-facing
Agent 4 (explore): Our codebase integration points
```

Each agent should return a structured report. Synthesize all reports into the architecture document.

**Agent Prompt Template:**
```
Explore the codebase at {path} and provide a thorough mapping of the {AREA} system.

Look at:
1. {directory1}/ - {what to look for}
2. {directory2}/ - {what to look for}
...

For each area, provide:
- What it does (2-3 sentences)
- Key files (just filenames, not full paths)
- Key exports/classes/functions
- How it relates to the overall architecture

Return your findings as a structured report with sections for each area.
```

---

## Configuration Audit Methodology

When auditing settings/configuration:

1. **Find all env vars:**
   ```
   Grep: "process\.env\." or "os\.environ" or "getenv"
   ```

2. **Find config files:**
   ```
   Glob: "**/.env*", "**/config.*", "**/settings.*", "**/*.config.*"
   ```

3. **Find CLI flags:**
   ```
   Grep: "option\(" or "addOption\(" or "argument\(" or "flag\("
   ```

4. **Find defaults:**
   ```
   Grep: "default:" or "DEFAULT_" or "defaultValue"
   ```

5. **Map each setting to our system:**
   - Do we have an equivalent?
   - Where is it configured? (env var, UI, config file)
   - What's the default?
   - Is it surfaced in our Settings UI?

---

## Quality Standards

### Architecture Document Quality
- Every major directory should be covered
- File tables should have clear, concise purpose descriptions
- "How it works" sections should explain the flow, not just list files
- Architecture diagram should show component relationships
- Settings table should be complete (no missing env vars)

### Comparison Document Quality
- Every component from the architecture doc must appear in comparison
- Winner column must be justified (not arbitrary)
- TW Location must be exact file paths
- Priority gaps must have realistic effort estimates
- "SKIP" items must have clear rationale

### Integration Plan Quality
- Tasks should be specific and actionable
- Task descriptions should explain WHAT and WHY
- Dependencies between tasks should be logical
- Final verification tasks should be comprehensive
- Phase should have clear acceptance criteria

---

## Example Usage

### Invocation
```
User: "I've downloaded ProjectX into /research/projectx-main. 
       Analyze it and create an integration plan."
```

### Expected Workflow
1. Read this SKILL.md
2. Explore codebase (4 parallel agents)
3. Create architecture map document
4. Create comparison document  
5. Determine next phase number
6. Create phase file + tasks in TASKS.md
7. Report summary to user

### Expected Output
- `docs/YYYYMMDD_HHMMSS_Cursor_PROJECTX_ARCHITECTURE_MAP.md`
- `docs/YYYYMMDD_HHMMSS_Cursor_PROJECTX_VS_GALDRWORKS_COMPARISON.md`
- `.galdr/phases/phase{N}_projectx-integration.md`
- Updated `.galdr/TASKS.md` with new phase and tasks

---

## Integration with Other Skills

| Skill | When to Chain |
|-------|--------------|
| `g-vault` | Write analysis summary to vault (Phase 4b — always do this) |
| `g-planning` | After creating integration plan, for detailed PRD if needed |
| `g-task-management` | For creating individual task files from the plan |
| `g-code-reviewer` | For reviewing integration code quality |
| `g-qa` | For tracking bugs discovered during integration |

---

## Templates

Templates for output documents are in:
- `reference/architecture_map_template.md`
- `reference/comparison_template.md`
- `reference/integration_phase_template.md`

---

*This skill systematizes the process of analyzing external codebases for integration into GaldrWorks. It ensures consistent, thorough analysis with no capabilities overlooked.*
