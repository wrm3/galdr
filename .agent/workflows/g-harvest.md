---
description: "Harvest ideas and improvements from external sources"
---

# Command: @g-harvest

## Purpose
Analyze an external source (repo, article, video, research) and present selective improvement suggestions. You choose what to adopt -- nothing changes without your approval.

## Usage
```
@g-harvest
```

Then provide the source when prompted, or include it inline:
```
@g-harvest I downloaded taskflow into research/taskflow-main
@g-harvest analyze this article: https://example.com/article
@g-harvest what can we learn from the transcript in docs/video_notes.md
```

## How It Works

### Step 1: Project Context
The system loads your current project state (SUBSYSTEMS.md, TASKS.md, PLAN.md) so it understands what you already have and what's planned.

### Step 2: Source Analysis
The external source is analyzed for capabilities, patterns, and ideas.

### Step 3: Harvest Menu
You receive a numbered menu of suggestions (max 15-20), each with:
- What it is and how it helps your project
- Effort estimate (Small / Medium / Large)
- Risk level (Low / Medium / High)
- Which of your subsystems would be affected
- Whether it overlaps with existing planned work

### Step 4: You Choose
Reply with:
- Specific numbers: "H-01, H-03, H-07"
- Questions: "tell me more about H-05"
- Modifications: "I want H-03 but done differently..."
- Pass: "none" to skip all
- (**Rarely**) "all" -- system will confirm before proceeding

### Step 5: Tasks Created
Only your approved items become tasks in `.galdr/TASKS.md`.
Each task is tagged `[Harvest: {source}]` for traceability.

## What This Command Does NOT Do

- Automatically integrate anything
- Create tasks without your approval
- Replace or restructure your existing systems
- Treat the external source as more important than your project
- Touch systems outside this project

## This Command vs. @g-analyze-codebase

| | @g-harvest | @g-analyze-codebase |
|---|---------------|------------------------|
| **For** | External sources (not yours) | Merging YOUR OWN projects |
| **Default** | Adopt nothing | Map everything |
| **User role** | Choose from menu | Approve integration plan |
| **Scope** | Only what you pick | Comprehensive merge |
| **Risk** | Low (controlled) | High (architectural) |

**Rule of thumb**: If you're browsing for ideas, use `@g-harvest`. If you're combining two of your own projects, use `@g-analyze-codebase`.

## Source Types Supported

| Source Type | Example |
|------------|---------|
| Repository | `research/some-project-main/` |
| Article/Blog | URL or saved document |
| Video transcript | Extracted transcript file |
| Research paper | PDF or markdown |
| Library docs | Documentation pages |
| Any text source | Notes, conversations, ideas |

## Related Commands

| Command | When to Use After |
|---------|-------------------|
| `@g-task-new` | Create individual task spec files for approved items |
| `@g-task-update` | Update task status during implementation |
| `@g-plan` | If harvest reveals need for a new phase |
| `@g-status` | Check current project state |
