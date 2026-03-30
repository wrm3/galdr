---
name: g-git-commit
description: Create well-structured git commits following galdr conventions, with proper type prefixes, task references, and agent footers for autonomous commits.
---
# galdr-git-commit

## When to Use
After completing a task, after any significant change, or @g-git-commit.

## Commit Message Format
```
{type}({subsystem}): {brief description}

{optional body — what changed and why}

Task: #{task_id}
Phase: {N}
```

## Commit Type Mapping
| Task Type | Commit Prefix |
|---|---|
| feature / task | `feat` |
| bug_fix | `fix` |
| refactor | `refactor` |
| documentation | `docs` |
| test | `test` |
| chore / config | `chore` |
| phase completion | `phase` |

## Steps

1. **Check what changed**:
   ```bash
   git status
   git diff --stat
   ```

2. **Stage relevant files**:
   ```bash
   git add .galdr/tasks/taskNNN_*.md
   git add .galdr/TASKS.md
   git add {changed source files}
   ```

3. **Compose message** using format above

4. **For autonomous agent commits**, add footer:
   ```
   Task: #NNN
   Phase: N
   Agent: {agent_id}
   Model: {model_name}
   Rules-Version: {version}
   ```

5. **Commit**:
   ```powershell
   git commit -m "$(cat <<'EOF'
   feat(api): implement task NNN
   
   Added JWT authentication middleware with refresh token support.
   
   Task: #103
   Phase: 1
   EOF
   )"
   ```
   
   On Windows PowerShell use single-line form or here-string carefully:
   ```powershell
   $msg = "feat(api): implement auth`n`nTask: #103`nPhase: 1"
   git commit -m $msg
   ```

## Phase Completion Commit
```bash
git add .galdr/phases/phaseN/ .galdr/TASKS.md .galdr/phases/phaseN_*.md
git commit -m "phase(N): Phase Name complete

Tasks completed: task001, task002, task003
Archived to: .galdr/phases/phaseN/
Subsystems: api, database"

git tag phase-N-complete
```
