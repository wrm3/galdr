# {Project Name} Architecture Map

> Complete component mapping of {project} codebase (`{source_path}`)
> Generated: {YYYY-MM-DD}

---

## Table of Contents

1. [Overview](#1-overview)
2. [Component 1](#2-component-1)
<!-- Add more as discovered -->

---

## 1. Overview

{Project Name} is {2-3 sentences describing what the project does, its primary purpose, and target users}.

**Tech Stack:**
- **Language:** {language} {version}
- **Runtime:** {runtime}
- **Package Manager:** {manager}
- **Build Tool:** {tool}
- **UI Framework:** {framework} (if applicable)

**Entry Point Flow:**
```
{entry_file} → {next_file} → {next_file} → {final destination}
```

**Default Ports:**
| Port | Service | Description |
|------|---------|-------------|
| {port} | {service_name} | {description} |

**Data Directory:** `{data_dir_path}`

---

## 2. {Component Name}

**Location:** `{relative_path}/`
**Purpose:** {2-3 sentences explaining what this component does and why it exists}

### Key Files

| File | Purpose |
|------|---------|
| `{filename}` | {What it does} |
| `{filename}` | {What it does} |

### How It Works

{3-5 sentence explanation of the component's flow and behavior}

### Configuration

| Setting | Default | Purpose |
|---------|---------|---------|
| `{SETTING_NAME}` | `{value}` | {What it controls} |

### Key Exports/Functions

| Export | Type | Purpose |
|--------|------|---------|
| `{name}` | function/class/interface | {What it does} |

---

<!-- Repeat Section 2 template for each component -->

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                  {Project Name}                      │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │Component1│  │Component2│  │Component3│          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│       │              │              │                │
│  ┌────▼──────────────▼──────────────▼──────────┐    │
│  │            Shared Infrastructure             │    │
│  └──────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

---

## Complete Settings/Config Reference

| Variable / Setting | Default | Source | Purpose |
|--------------------|---------|--------|---------|
| `{SETTING}` | `{default}` | env/config/cli | {purpose} |

---

*Document generated from {source_path} codebase analysis*
*Total source files: ~{count}*
