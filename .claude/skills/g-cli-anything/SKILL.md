---
name: g-cli-anything
description: "Build or install CLI harnesses for GUI applications. Turns desktop software into stateful, agent-usable CLIs with structured JSON output."
---

# g-cli-anything

Build or install agent-native CLI interfaces for GUI applications using the
[CLI-Anything](https://github.com/HKUDS/CLI-Anything) methodology (Apache 2.0, HKUDS).

## When to Use

- Agent needs to operate a GUI application (Blender, GIMP, Audacity, OBS, etc.) programmatically
- Building a new CLI harness for software that doesn't have one yet
- Installing a pre-built harness from the CLI-Hub registry
- Agent needs structured JSON output from desktop software operations

## Pre-Built Harnesses (Install & Use)

### Registry Discovery

The CLI-Hub registry at `research/CLI-Anything-main/registry.json` catalogs 25+ harnesses.
Install any with:

```bash
# From local checkout
uv pip install -e research/CLI-Anything-main/<software>/agent-harness

# From GitHub
uv pip install "git+https://github.com/HKUDS/CLI-Anything.git#subdirectory=<software>/agent-harness"
```

### Available Harnesses (Partial List)

| Software | Category | Entry Point | Prerequisites |
|----------|----------|-------------|---------------|
| Blender | 3D | `cli-anything-blender` | blender on PATH |
| GIMP | Image | `cli-anything-gimp` | gimp on PATH |
| Audacity | Audio | `cli-anything-audacity` | sox |
| Shotcut | Video | `cli-anything-shotcut` | melt (MLT) |
| OBS Studio | Streaming | `cli-anything-obs` | OBS + WebSocket |
| LibreOffice | Office | `cli-anything-libreoffice` | soffice on PATH |
| Krita | Image | `cli-anything-krita` | krita on PATH |
| Inkscape | Vector | `cli-anything-inkscape` | inkscape on PATH |
| Browser | Web | `cli-anything-browser` | Node.js + Chrome + DOMShell |
| ComfyUI | AI Art | `cli-anything-comfyui` | ComfyUI server |
| Ollama | LLM | `cli-anything-ollama` | ollama on PATH |
| Mermaid | Diagrams | `cli-anything-mermaid` | mmdc (mermaid-cli) |

### Using an Installed Harness

```bash
# One-shot command with JSON output (for agent consumption)
cli-anything-<software> --json <command-group> <subcommand> [args]

# Interactive REPL (for exploration)
cli-anything-<software>

# Help
cli-anything-<software> --help
```

Every harness follows the same patterns:
- `--json` flag for machine-readable output on all commands
- Subcommand groups matching the app's logical domains
- REPL mode when invoked with no arguments
- Session/state management for multi-step workflows

## Building a New Harness (7-Phase Pipeline)

When no pre-built harness exists, follow this pipeline to create one.
Full SOP: `research/CLI-Anything-main/cli-anything-plugin/HARNESS.md`

### Phase 1: Codebase Analysis

1. Identify the backend engine (e.g., MLT for Shotcut, ImageMagick for GIMP)
2. Map GUI actions to API calls — every button maps to a function
3. Identify the data model (XML, JSON, binary, database?)
4. Find existing CLI tools the backend ships (`melt`, `ffmpeg`, `convert`)
5. Catalog the command/undo system

### Phase 2: CLI Architecture Design

1. Choose interaction model: **stateful REPL + subcommand CLI** (recommended: both)
2. Define command groups matching the app's domains:
   - Project management (new, open, save, close)
   - Core operations (the app's primary purpose)
   - Import/Export (file I/O, format conversion)
   - Configuration (settings, preferences)
   - Session/State (undo, redo, history, status)
3. Design state model (what persists between commands, JSON session files)
4. Plan output: human-readable (tables) + machine-readable (JSON via `--json`)

### Phase 3: Implementation

Directory structure:
```
<software>/agent-harness/
├── setup.py
└── cli_anything/          # Namespace package (NO __init__.py)
    └── <software>/        # Sub-package (HAS __init__.py)
        ├── <software>_cli.py   # Click CLI entry point
        ├── core/               # Domain model modules
        ├── utils/              # Backend wrappers, repl_skin.py
        ├── skills/SKILL.md     # Agent-discoverable skill
        └── tests/
```

Key patterns:
- **Click** for CLI framework (`click>=8`)
- **prompt-toolkit** for REPL (`prompt-toolkit>=3`)
- `--json` global flag switching output format
- Session singleton for state management
- `utils/<software>_backend.py` wraps real software invocation via `subprocess.run()`
- Namespace package: `cli_anything/` has NO `__init__.py` (PEP 420)

### Phase 4: Test Planning

Create `TEST.md` before writing test code. Plan unit tests (synthetic data),
E2E tests (real files + real software), and workflow scenarios.

### Phase 5: Test Implementation

- Unit tests: `test_core.py` — every core function, no external deps
- E2E tests: `test_full_e2e.py` — invoke real software, verify output
- CLI subprocess tests: use `_resolve_cli("cli-anything-<software>")` pattern
- Output verification: magic bytes, format validation, content checks

### Phase 6: Documentation

Run `pytest -v --tb=no`, append results to TEST.md.

### Phase 6.5: SKILL.md Generation

Generate `cli_anything/<software>/skills/SKILL.md` with YAML frontmatter
and command documentation for agent discovery.

### Phase 7: Packaging

```python
# setup.py
setup(
    name="cli-anything-<software>",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    entry_points={"console_scripts": ["cli-anything-<software>=cli_anything.<software>.<software>_cli:main"]},
    install_requires=["click>=8.0.0", "prompt-toolkit>=3.0.0"],
    python_requires=">=3.10",
)
```

Install: `uv pip install -e .`
Verify: `cli-anything-<software> --help`

## Installed Harnesses in This Project

### cli-anything-blender

Stateful CLI for 3D scene editing via JSON scene descriptions + bpy script generation.

**Command groups**: scene, object, material, modifier, lighting, animation, render

```bash
cli-anything-blender --json scene new --name "MyScene"
cli-anything-blender --json object add cube --name "MyCube" --location 0,0,1
cli-anything-blender --json material create --name "Red" --color 1,0,0,1
cli-anything-blender --json render setup --engine CYCLES --resolution 1920x1080
cli-anything-blender --json render execute -p scene.json -o output.png
```

**When to use vs Blender MCP**: The CLI harness works via JSON scene files and subprocess
invocation of `blender --background --python`. Use it for batch operations, scripted
pipelines, and when you need portable scene descriptions. The Blender MCP server
provides direct bpy API access for real-time interactive work.

### cli-anything-browser

Filesystem-first browser automation via DOMShell's Accessibility Tree.

**Command groups**: page, fs, act, session

```bash
cli-anything-browser page open https://example.com
cli-anything-browser --json fs ls /
cli-anything-browser fs grep "Login"
cli-anything-browser act click /main/button[0]
cli-anything-browser act type /main/input[0] "user@example.com"
```

**Prerequisites**: Node.js/npx, Chrome with DOMShell extension installed.

**When to use vs cursor-ide-browser MCP**: The CLI harness uses DOMShell which maps
Chrome's Accessibility Tree to a virtual filesystem (ls/cd/cat/grep). Best for
structured page exploration and accessibility-first automation. The cursor-ide-browser
MCP uses Playwright for DOM-level interaction with screenshots and profiling. Use
cursor-ide-browser for visual testing; use cli-anything-browser for structured
data extraction and accessibility-tree navigation.

## References

- **Upstream repo**: https://github.com/HKUDS/CLI-Anything
- **License**: Apache 2.0
- **Full SOP**: `research/CLI-Anything-main/cli-anything-plugin/HARNESS.md`
- **Registry**: `research/CLI-Anything-main/registry.json`
- **CLI-Hub**: https://hkuds.github.io/CLI-Anything/
