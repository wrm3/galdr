# galdr Skills Reference

Skills are the engine behind every command and agent. Each skill owns a specific domain and provides detailed, step-by-step workflows.

## Naming Convention

All galdr skills use the `g-skl-{name}` folder prefix. The entry point is always `SKILL.md` inside that folder.

---

## Core galdr Skills (File-Centric Architecture)

Each skill "owns" specific `.galdr/` files. Only its owner skill should write to those files.

| Skill | Owns | Description |
|-------|------|-------------|
| `g-skl-tasks` | `TASKS.md`, `tasks/` | Task creation, status updates, sync check, complexity scoring, sprint planning |
| `g-skl-bugs` | `BUGS.md`, `bugs/` | Bug reporting, bug fixes, quality metrics |
| `g-skl-ideas` | `IDEA_BOARD.md` | Idea capture, review, promotion to tasks, proactive scanning |
| `g-skl-plan` | `PLAN.md`, `PRDS.md`, `prds/` | Plan creation, PRD writing, phase management |
| `g-skl-project` | `PROJECT.md`, `CONSTRAINTS.md` | Project identity, goals, architectural constraints |
| `g-skl-subsystems` | `SUBSYSTEMS.md`, `subsystems/` | Subsystem discovery, spec creation, activity logging, sync |
| `g-skl-medkit` | `.galdr/` (all files) | Health check, structural repair, version migration, routine maintenance |
| `g-skl-setup` | `.galdr/.identity` (initial) | First-time galdr initialization |

---

## Workflow Skills

| Skill | Description |
|-------|-------------|
| `g-skl-code-review` | Security, quality, performance review. Scales from quick scan to full architecture audit. |
| `g-skl-status` | Project status — session context, active tasks, goals, ideas |
| `g-skl-sprint` | Autonomous 2-hour sprint execution |
| `g-skl-git-commit` | Well-structured commits following galdr conventions |
| `g-skl-harvest` | Analyze external sources and propose selective improvements |
| `g-skl-report` | Project health report generation |
| `g-skl-swot-review` | Automated SWOT analysis for the current project phase |
| `g-skl-verify-ladder` | Multi-level verification gates for completed tasks |

---

## Cross-Project Skills

| Skill | Description |
|-------|-------------|
| `g-skl-broadcast` | Push tasks to child projects with cascade depth |
| `g-skl-peer-sync` | Sync shared contracts with sibling projects |
| `g-skl-request` | Child project requests parent action |
| `g-skl-inbox` | Review and action cross-project coordination queue |
| `g-skl-graph` | Assemble and display the project ecosystem graph (3 hops) |
| `g-skl-topology` | View or edit cross-project topology declarations |

---

## Development Skills

| Skill | Description |
|-------|-------------|
| `database-standards` | Oracle, MySQL, PostgreSQL naming and coding conventions |
| `github-integration` | GitHub repos, issues, PRs, Actions, gh CLI |
| `mcp-builder` | MCP server development with FastMCP |
| `cicd-pipelines` | CI/CD for GitHub Actions, GitLab CI, Jenkins |
| `kubernetes-operations` | K8s cluster management, kubectl, Helm |
| `portainer-management` | Container management via Portainer |
| `cloud-engineering` | AWS, GCP, Azure architecture and IaC |
| `ai-ml-development` | Model training, RLHF, RAG, MLOps |
| `web3-blockchain` | EVM, Solana, Solidity, DeFi, NFTs |
| `research-methodology` | Deep multi-source research and synthesis |

---

## Video & 3D Skills

| Skill | Description |
|-------|-------------|
| `remotion-video` | Programmatic video creation in React |
| `manim-animation` | Mathematical animations (3Blue1Brown style) |
| `storyboard-creation` | Film/video storyboarding |
| `ai-video-generation` | AI video with 40+ models (Veo, Wan, Seedance, etc.) |
| `ai-avatar-lipsync` | AI avatars and talking head videos |
| `animation-principles` | Disney's 12 principles for interactive 3D |
| `algorithmic-art` | Generative art with p5.js |
| `explainer-video` | Explainer video production workflow |
| `3d-performance` | 3D web scene optimization (LOD, culling, draw calls) |
| `asset-optimization` | GLB/GLTF compression pipeline |

---

## Business & Startup Skills

| Skill | Description |
|-------|-------------|
| `startup-business-formation` | Delaware C-Corp, entity choice, equity, 83(b) |
| `startup-vc-fundraising` | VC fundraising, pitch decks, term sheets |
| `startup-product-development` | MVP, roadmaps, PMF, build vs buy |
| `startup-resource-access` | Cloud credits, accelerators, grants |
| `business-operations` | HR, payroll, compensation, finance |
| `nonprofit-formation` | 501(c)(3), tax-exempt formation |
| `patent-filing-ai` | AI/ML patents, provisional and utility |

---

## IDE & Config Skills

| Skill | Description |
|-------|-------------|
| `cursor-project-config` | Maintain .cursor/ IDE configuration |
| `claude-code-project-config` | Maintain .claude/ project configuration |
| `cursor-cli` | Cursor CLI (`agent`) modes and API |
| `claude-cli` | Claude Code CLI flags and sessions |
| `gemini-cli` | Gemini CLI reference |
| `skill-creator` | Author new skills following galdr conventions |
| `agent-creator` | Create new agent definitions |
| `project-setup` | Scaffold new repositories |

---

## Knowledge & Vault Skills

| Skill | Description |
|-------|-------------|
| `g-skl-vault` | Read/write vault notes across projects |
| `g-skl-knowledge-refresh` | Audit vault freshness, re-fetch expired sources |
| `g-skl-platform-crawl` | Crawl docs and web with crawl4ai |
| `youtube-video-analysis` | YouTube metadata, transcript, vision analysis |
