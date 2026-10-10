# Sprint Guardian — Deployment Guide

This guide covers production deployment options for Sprint Guardian.

---

## Deployment Options at a Glance

| Deployment Target | Best For | Prerequisites |
|---|---|---|
| **Option 1: Docker / Compose** | Always-on containers, isolated environments, Kubernetes | Docker & Docker Compose |
| **Option 2: Linux / macOS VM** | Dedicated internal servers, system cron | Python 3.8+, Node.js (npx) |
| **Option 3: GitHub Actions** | Serverless automation without dedicated servers | GitHub Repository & Secrets |
| **Option 4: Local Developer CLI** | Individual Scrum Masters & Tech Leads | Codex CLI / Claude Code |

---

## Option 1: Docker / Docker Compose Deployment

Containerized deployment is the recommended approach for continuous, isolated server environments.

### 1. Configure Environment
```bash
cp .env.example .env
cp references/team-map.example.yaml references/team-map.local.yaml
# Edit .env and references/team-map.local.yaml with your Jira details
```

### 2. Build & Launch Scheduled Cron Daemon
```bash
docker compose up -d sprint-guardian
```
The container will launch, run pre-flight environment checks, install the cron schedule, and run in the background.

### 3. Check Logs
```bash
docker compose logs -f sprint-guardian
```

### 4. Run One-Off Commands via Docker
```bash
# Generate standup brief
docker compose run --rm sprint-guardian-cli standup-brief

# Inspect sprint health
docker compose run --rm sprint-guardian-cli inspect-sprint --sprint-id 4567

# Triage backlog queue
docker compose run --rm sprint-guardian-cli triage-queue
```

---

## Option 2: Linux / macOS Server (Cron Deployment)

Deploy directly onto a team server or VM running 24/7.

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/your-org/sprint-guardian.git
cd sprint-guardian

# Run interactive setup wizard
./automation/setup.sh

# Install Python requirements
pip install -r requirements.txt
```

### 2. Verify MCP & Jira Connectivity
```bash
python3 scripts/verify_mcp_connection.py
```

### 3. Install Automated Crontab
```bash
./scripts/install_cron.sh
```
This script dynamically detects your repository path, writes the schedules into your crontab, and redirects outputs to `automation/output/cron-logs/`.

To inspect active cron schedules:
```bash
crontab -l
```

---

## Option 3: Serverless GitHub Actions Deployment

If your team does not maintain an always-on server, Sprint Guardian can run entirely serverless via GitHub Actions.

### 1. Configure GitHub Repository Secrets
Navigate to **Settings > Secrets and variables > Actions** in your GitHub repo and add:
- `JIRA_INSTANCE_URL`: `https://your-domain.atlassian.net`
- `JIRA_EMAIL`: `your-service-account@example.com`
- `JIRA_API_TOKEN`: `your-atlassian-api-token`
- `JIRA_BOARD_ID`: `1234`
- `JIRA_PROJECT_KEY`: `PROJ`

### 2. Scheduled Ceremonies
The included workflow [`.github/workflows/scheduled-sprint-guardian.yml`](../.github/workflows/scheduled-sprint-guardian.yml) triggers automatically:
- **Every Monday at 9:00 AM UTC**: Sprint Scope Shaping
- **Weekdays at 9:30 AM UTC**: Daily Standup Brief
- **Tuesday & Thursday at 4:00 PM UTC**: Delivery Risk Surface

Outputs and reports are archived as workflow artifacts downloadable directly from GitHub.

---

## Option 4: Local Developer / Scrum Master CLI

For individual Scrum Masters or Project Leads who want to run Sprint Guardian interactively:

### 1. Install Skill
```bash
./automation/install-skill.sh
```
This symlinks the skill folder into `~/.codex/skills/` and `~/.claude/skills/`.

### 2. Run Interactively
```bash
# Read-only sprint inspection
./automation/inspect-sprint.sh

# Recommend assignees
./automation/suggest-owner.sh --issue-keys "PROJ-101"

# Apply reassignment with approval
./automation/suggest-owner.sh \
  --issue-keys "PROJ-101" \
  --apply \
  --approved-by "Coder Coder"
```

---

## Production Security Checklist

Before deploying in a production environment:

- [ ] **Dry-Run by Default**: Ensure `--apply` is never used in unattended cron scripts unless specifically audited.
- [ ] **Authority Roster**: Verify that only authorized Project Leads/Engineering Managers are listed in `approval.assigning_authorities` in `references/team-map.local.yaml`.
- [ ] **Secrets Protection**: Confirm `.env` and `references/team-map.local.yaml` are excluded from version control (verified in `.gitignore`).
- [ ] **Audit Trail**: Monitor `automation/output/approvals.log` regularly to audit all applied Jira changes.
- [ ] **WIP Limit Adherence**: Configure accurate `max_in_progress` limits for all developers in the team map to prevent AI overallocation.

---

*[Back to README](../README.md)*
