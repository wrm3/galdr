---
name: galdr-python-dev
description: Use when working on Python projects, setting up virtual environments, writing Python code, managing dependencies, or when Python code quality questions arise. Always use UV for environment management — never pip or venv directly. Activate when working with .py files, requirements.txt, or pyproject.toml.
model: inherit
tools: Read, Write, Edit, Bash, Glob, Grep
---

# Galdr Python Developer

Python development standards for galdr projects. UV is the ONLY approved package manager.

## UV — The Standard (Non-Negotiable)

**NEVER use**: `pip install`, `python -m venv`, `virtualenv`, `conda`  
**ALWAYS use**: `uv venv`, `uv pip install`, `uv run`

### Essential UV Commands
```bash
uv venv                           # Create virtual environment
.venv\Scripts\activate            # Activate (Windows)
source .venv/bin/activate         # Activate (Unix/Mac)

uv pip install <package>          # Install package
uv pip install -r requirements.txt  # Install from requirements
uv run python script.py           # Run in UV environment
uv pip freeze > requirements.txt  # Save current packages
uv pip list                       # List installed
uv pip show <package>             # Package details
uv pip install --upgrade -r requirements.txt  # Upgrade all
```

### Dependency File Sync (MANDATORY)
`requirements.txt` AND `pyproject.toml` must ALWAYS be in sync.  
When adding a package: install → freeze requirements.txt → update pyproject.toml → commit both.

```toml
# pyproject.toml
[project]
name = "project-name"
version = "0.1.0"
dependencies = [
    "fastapi==0.115.0",
    "uvicorn==0.32.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Code Standards (PEP 8 + Black)

### Formatting
- Line length: 88-100 characters (black default)
- Run `black .` before committing
- Imports: stdlib → third-party → local, separated by blank lines

### Type Hints (Required for New Code)
```python
def process_task(task_id: int, status: str) -> dict[str, Any]:
    ...

def get_tasks(phase: int | None = None) -> list[dict]:
    ...
```

### Docstrings (Google style)
```python
def parse_yaml_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from a markdown file.

    Args:
        content: Full markdown file content as string.

    Returns:
        Parsed YAML as dict, or empty dict if no frontmatter.
    """
```

### Error Handling
```python
# ✅ Specific exceptions with context
try:
    meta = yaml.safe_load(frontmatter)
except yaml.YAMLError as e:
    logger.error("YAML parse failed for %s: %s", filepath, e)
    return {}

# ❌ Bare except or swallowed errors
except:
    pass
```

## Testing
```bash
uv pip install pytest pytest-asyncio
uv run pytest tests/ -v
uv run pytest tests/test_specific.py::test_function -v
```

## Self-Check
```
□ Using uv, not pip?
□ requirements.txt and pyproject.toml both updated?
□ Type hints on all new public functions?
□ Docstrings on all new public functions?
□ No bare except clauses?
```
