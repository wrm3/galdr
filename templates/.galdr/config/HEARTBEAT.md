---
enabled: {true|false}
timezone: {IANA_timezone}
max_concurrent_agents: {n}
budget_limit_daily_usd: {amount}
default_adapter: {claude|cursor|gemini}
---

# HEARTBEAT.md — {project_name}

Configure scheduled galdr routines. Each routine is a `###` heading with **Schedule**, **Agent**, **Skill**, **Enabled**, and **Description**.

## Routines

### {routine_name}
- **Schedule**: {cron_minute hour day month weekday}
- **Agent**: {agent_id}
- **Skill**: {skill_name}
- **Enabled**: {true|false}
- **Description**: {what this routine does}
