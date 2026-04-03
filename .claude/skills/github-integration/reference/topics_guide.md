# GitHub Repository Topics - Best Practices Guide

Complete guide for managing GitHub repository topics effectively.

## What Are Repository Topics?

Repository topics are tags that help users discover your project on GitHub. They improve discoverability through:
- GitHub's topic-based search
- Topic pages (e.g., github.com/topics/machine-learning)
- Repository recommendations
- GitHub Explore features

## Topic Format Rules

### Technical Requirements

**Format:**
- Lowercase letters only
- Numbers allowed
- Hyphens allowed (use as word separators)
- No spaces, underscores, or special characters
- Maximum 50 characters per topic
- Maximum 20 topics per repository

**Valid Topics:**
```
✅ claude-code
✅ ai-assistant
✅ python3
✅ web-scraping
✅ task-management
```

**Invalid Topics:**
```
❌ Cursor IDE (spaces)
❌ AI_Assistant (underscores)
❌ web.scraping (periods)
❌ MACHINE-LEARNING (uppercase)
❌ @automation (special characters)
```

### Normalization Process

When users provide topics in natural language, normalize them:

```
User Input → Normalized Topic
"Cursor IDE" → "cursor-ide"
"AI Assistant" → "ai-assistant"
"Web Scraping" → "web-scraping"
"Task Management" → "task-management"
"Python 3.11" → "python3"
"Machine Learning" → "machine-learning"
```

## Topic Categories

### 1. Platform/IDE Topics

Identify the primary platforms or IDEs your project supports:

```
# AI Assistant Platforms
cursor-ide        # Cursor IDE
cursor            # Cursor IDE
cursor-ide        # Alternative for Cursor
windsurf          # Windsurf IDE
roo-code          # Roo-Code IDE
copilot           # GitHub Copilot

# Traditional IDEs
vscode            # Visual Studio Code
intellij          # IntelliJ IDEA
pycharm           # PyCharm
vim               # Vim/Neovim
```

### 2. AI/ML Topics

For AI and machine learning projects:

```
# AI Companies/Models
anthropic         # Anthropic (Claude)
openai            # OpenAI (GPT)
claude            # Claude models
gpt               # GPT models

# AI Categories
ai-assistant      # AI assistant tools
llm               # Large Language Models
machine-learning  # ML projects
deep-learning     # Deep learning
nlp               # Natural Language Processing
computer-vision   # Computer vision

# AI Applications
ai-agent          # AI agents
chatbot           # Chatbots
code-generation   # Code generation
```

### 3. Programming Language Topics

Always include your primary language(s):

```
# Languages
python            # Python
javascript        # JavaScript
typescript        # TypeScript
java              # Java
rust              # Rust
go                # Go
ruby              # Ruby
php               # PHP
csharp            # C#
cpp               # C++
```

### 4. Framework/Library Topics

Include major frameworks and libraries:

```
# Web Frameworks
react             # React
nextjs            # Next.js
vue               # Vue.js
angular           # Angular
django            # Django
flask             # Flask
fastapi           # FastAPI
express           # Express.js

# Testing
pytest            # Pytest
jest              # Jest
selenium          # Selenium
playwright        # Playwright

# Data Science
pandas            # Pandas
numpy             # NumPy
tensorflow        # TensorFlow
pytorch           # PyTorch
```

### 5. Purpose/Category Topics

Describe what your project does:

```
# Project Types
automation        # Automation tools
integration       # Integration projects
template          # Project templates
boilerplate       # Boilerplate code
starter-kit       # Starter kits
library           # Libraries
framework         # Frameworks
cli-tool          # CLI tools
api               # APIs

# Functionality
task-management   # Task management
web-scraping      # Web scraping
data-analysis     # Data analysis
documentation     # Documentation
testing           # Testing tools
deployment        # Deployment tools
monitoring        # Monitoring tools
```

### 6. Domain/Industry Topics

Specify the domain or industry:

```
# Development Tools
devtools          # Developer tools
productivity      # Productivity tools
developer-tools   # Alternative for devtools

# Industries
finance           # Finance
healthcare        # Healthcare
education         # Education
ecommerce         # E-commerce

# Use Cases
enterprise        # Enterprise solutions
personal          # Personal projects
education         # Educational projects
research          # Research projects
```

### 7. Integration Topics

List services and platforms you integrate with:

```
# Atlassian
jira              # Jira
jira-integration  # Jira integration
confluence        # Confluence
bitbucket         # Bitbucket
trello            # Trello

# Version Control
github            # GitHub
gitlab            # GitLab
git               # Git

# Cloud Platforms
aws               # Amazon Web Services
azure             # Microsoft Azure
gcp               # Google Cloud Platform

# Databases
mysql             # MySQL
postgresql        # PostgreSQL
mongodb           # MongoDB
redis             # Redis

# Other Services
slack             # Slack
discord           # Discord
notion            # Notion
```

### 8. Protocol/Standard Topics

Include relevant protocols and standards:

```
# Protocols
mcp               # Model Context Protocol
rest-api          # REST API
graphql           # GraphQL
websocket         # WebSocket
grpc              # gRPC

# Standards
oauth             # OAuth
jwt               # JWT (JSON Web Tokens)
openapi           # OpenAPI
json-schema       # JSON Schema
```

## Recommended Topic Counts

### By Project Type

**Personal Projects:** 5-10 topics
- Focus on core technologies and purpose
- Example: python, automation, task-management, cli-tool, personal

**Open Source Libraries:** 8-12 topics
- Include language, framework, category, and use cases
- Example: python, fastapi, rest-api, authentication, jwt, oauth, library, middleware

**Enterprise Tools:** 10-15 topics
- Comprehensive coverage of integrations and features
- Example: claude-code, cursor, ai-assistant, anthropic, task-management, jira-integration, confluence, automation, enterprise, mcp

**Boilerplate/Templates:** 8-12 topics
- Platform, languages, frameworks, and purpose
- Example: claude-code, cursor, template, boilerplate, python, typescript, mcp, task-management

## Topic Selection Strategy

### Step 1: Identify Core Topics (3-5)

These are non-negotiable, primary identifiers:

```
Example for Cursor Project:
1. cursor-ide (platform)
2. cursor (platform)
3. ai-assistant (category)
4. anthropic (company)
5. python (language)
```

### Step 2: Add Feature Topics (2-4)

Describe main features:

```
Example:
1. task-management
2. automation
3. mcp (if using MCP)
4. web-scraping (if applicable)
```

### Step 3: Add Integration Topics (1-3)

List major integrations:

```
Example:
1. jira-integration
2. github
3. confluence
```

### Step 4: Add Niche/Specific Topics (1-3)

Help users find your specific use case:

```
Example:
1. desktop-automation
2. browser-automation
3. documentation-generator
```

### Total: 7-15 topics (ideal range)

## Topic Research Methods

### Method 1: Check Similar Projects

1. Find popular similar projects on GitHub
2. Review their topics
3. Adopt established, popular topics

```bash
# View topics for a repository
gh repo view owner/repo --json repositoryTopics
```

### Method 2: Browse Topic Pages

Visit GitHub topic pages to see:
- How many repos use the topic
- What other topics are commonly paired
- If topic name is established

```
https://github.com/topics/claude-code
https://github.com/topics/ai-assistant
https://github.com/topics/task-management
```

### Method 3: GitHub Search

Search for similar projects and analyze their topics:

```
# On GitHub
site:github.com "claude code" automation
```

## Topic Maintenance

### When to Update Topics

**Add Topics When:**
- ✅ Adding new integrations
- ✅ Supporting new platforms
- ✅ Adding major features
- ✅ Expanding to new use cases

**Remove Topics When:**
- ✅ Deprecating features
- ✅ Removing integrations
- ✅ Pivoting project focus
- ✅ Too many topics (over 15)

**Update Topics When:**
- ✅ Community adopts different naming
- ✅ Official topic names emerge
- ✅ Rebranding occurs

### Topic Review Schedule

**Monthly:** Quick review for new features
**Quarterly:** Comprehensive review of all topics
**Yearly:** Complete topic strategy review

## Common Mistakes to Avoid

### 1. Too Generic
```
❌ "software" - Too broad, not helpful
❌ "tool" - Too vague
✅ "task-management-tool" - Specific and searchable
```

### 2. Too Specific
```
❌ "jira-issue-creation-automation-v2" - Too narrow
✅ "jira-automation" - Balanced specificity
```

### 3. Redundant Topics
```
❌ python, python3, python-3, py - Pick one
✅ python - Sufficient
```

### 4. Brand/Product Names as Topics
```
⚠️ Use carefully - may confuse users
✅ jira (widely known)
❌ my-company-product (unknown)
```

### 5. Uppercase or Spaces
```
❌ "Machine Learning"
❌ "PYTHON"
✅ "machine-learning"
✅ "python"
```

## Topic Examples by Project Type

### AI Assistant Integration Project
```
Core: claude-code, cursor, ai-assistant, anthropic
Features: task-management, automation, mcp
Integrations: jira-integration, github, confluence
Language: python, typescript
Total: 11 topics
```

### Web Scraping Tool
```
Core: web-scraping, automation, python
Features: browser-automation, data-extraction
Libraries: selenium, playwright, beautifulsoup
Purpose: cli-tool, library
Total: 9 topics
```

### React Component Library
```
Core: react, component-library, typescript
Features: ui-components, design-system
Purpose: library, npm-package
Styling: css-in-js, styled-components
Total: 8 topics
```

### Task Management System
```
Core: task-management, project-management
Features: kanban, agile, collaboration
Tech: python, fastapi, react
Purpose: productivity, team-tool
Total: 9 topics
```

### MCP Server
```
Core: mcp, mcp-server, claude-code
Features: automation, api-integration
Language: python, typescript
Purpose: ai-tools, developer-tools
Total: 8 topics
```

## GitHub CLI Commands for Topics

### View Current Topics
```bash
gh repo view --json repositoryTopics --jq '.repositoryTopics[].name'
```

### Add Topics
```bash
# Add single topic
gh repo edit --add-topic claude-code

# Add multiple topics
gh repo edit --add-topic claude-code,cursor,ai-assistant

# Add topics preserving existing
gh repo edit --add-topic new-topic1,new-topic2
```

### Remove Topics
```bash
# Remove single topic
gh repo edit --remove-topic old-topic

# Remove multiple topics
gh repo edit --remove-topic topic1,topic2
```

### Replace All Topics
```bash
# This requires getting current topics first, then setting new ones
# GitHub CLI adds to existing, doesn't replace
# To replace: remove old, then add new
gh repo edit --remove-topic old1,old2
gh repo edit --add-topic new1,new2,new3
```

## Best Practices Summary

**DO:**
1. ✅ Use 7-15 topics (ideal range)
2. ✅ Research similar projects for established topics
3. ✅ Include primary language and platform
4. ✅ Use hyphens for multi-word topics
5. ✅ Keep topics lowercase
6. ✅ Update topics as project evolves
7. ✅ Prioritize searchability over uniqueness
8. ✅ Test topics by searching GitHub

**DON'T:**
1. ❌ Use all 20 topic slots
2. ❌ Use spaces or underscores
3. ❌ Create brand new topic names without research
4. ❌ Include redundant topics
5. ❌ Use overly generic topics ("software", "tool")
6. ❌ Use overly specific topics ("my-specific-feature-v2")
7. ❌ Forget to update topics when pivoting
8. ❌ Use uppercase letters

## Resources

- **GitHub Topic Search:** https://github.com/topics
- **GitHub Docs:** https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics
- **Topic Suggestions:** GitHub's autocomplete when adding topics
- **Popular Topics:** Browse https://github.com/topics to see trending topics

---

**Remember:** Topics are for discovery, not for SEO spam. Choose topics that accurately represent your project and help users find what they need.
