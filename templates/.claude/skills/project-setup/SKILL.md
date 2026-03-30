---
name: project-setup
description: Scaffold new repos—folders, git, docs, Cursor config, galdr tasks, MCP setup.
---

# Project Setup Skill

## Overview
This Skill helps initialize new projects with standardized structure, documentation templates, and configuration files for multiple AI IDEs.

## Capabilities
- Create standard folder structure
- Initialize git repository
- Set up AI assistant configurations (Cursor)
- Create documentation templates
- Initialize task management system
- Set up MCP tool configurations

## Standard Project Structure
```
project-name/
├── README.md                    # Project documentation
├── .gitignore                   # Git ignore rules
├── .cursor/                     # Cursor IDE config
│   ├── agents/
│   ├── commands/
│   ├── skills/
│   └── rules/
├── .galdr/            # Task management
│   ├── tasks/
│   ├── phases/
│   ├── TASKS.md
│   └── PLAN.md
├── docs/                        # Documentation
└── temp_scripts/                # Test scripts
```

## When to Use
Use this Skill when:
- Starting a new project from scratch
- Converting an existing project to use AI assistant tools
- Setting up standardized development environment
- Creating project templates
- User mentions: "new project", "initialize", "setup", "scaffold"

## Setup Process

### 1. Create Base Structure
```bash
# Create main folders
mkdir -p docs temp_scripts

# Create Cursor IDE configurations
mkdir -p .cursor/agents .cursor/commands .cursor/skills .cursor/rules
```

### 2. Initialize Git
```bash
git init
# Create .gitignore with common patterns
```

### 3. Create Documentation
- README.md - Project overview
- docs/ folder for additional documentation

### 4. Initialize Task Management
Use MCP tool: `galdr_tasks_setup` to initialize the task management system

### 5. Create Initial Files
- Project context documentation
- Basic configuration files
- Example templates

## Configuration Templates

### .gitignore Template
```
# Dependencies
node_modules/
venv/
__pycache__/

# IDE
.vscode/
.idea/

# Environment
.env
.env.local

# Build outputs
dist/
build/
*.pyc

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db
```

### README.md Template
```markdown
# Project Name

## Description
Brief description of the project

## Setup
Installation and setup instructions

## Usage
How to use the project

## Development
Development guidelines and commands

## License
License information
```

## Best Practices
- Always create a comprehensive .gitignore
- Document the project structure in CLAUDE.md
- Set up task management from the start
- Include example configurations
- Create clear README with setup instructions
- Initialize version control early

## Resources
This Skill works with:
- galdr_tasks MCP tool for task management
- Git for version control
- Multiple AI IDE configurations

