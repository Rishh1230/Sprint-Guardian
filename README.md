# 🛡️ Sprint Guardian

> **An AI-powered Agile Sprint Orchestrator that automates Jira task triage, load balancing, and team standups with secure, human-in-the-loop guardrails.**


---

## 📖 Overview

**Sprint Guardian** is a developer-centric Agile automation system that bridges the gap between Large Language Models (LLMs) and project management platforms. Powered by the **Model Context Protocol (MCP)**, it acts as an intelligent co-pilot for Scrum Masters and Project Leads.

The agent automatically inspects Jira sprint health, balances developer workloads based on team capacities, flags delivery risks, and drafts team standups — all while keeping write actions behind a **secure human approval gate**.

By automating repetitive coordination tasks, Sprint Guardian reduces manual Jira overhead and helps team leads focus on **delivery** rather than ticket management.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔀 **9 Operational Modes** | Dedicated workflows for sprint planning, queue triaging, standup compilation, workload balancing, and retrospectives |
| ⚖️ **Dynamic Workload Balancing** | Analyzes active sprint data, identifies overloaded developers, and proposes reassignment recommendations adhering to WIP limits |
| 🔐 **Approval-Gated Governance** | Built-in safety guardrails prevent AI from mutating Jira tickets without an authorized human's `approved-by` signature |
| 📋 **Agile Ceremony Automation** | Instantly generates daily standup briefs, sprint retrospective drafts, and backlog queue triaging notes |
| 🔗 **Real-time Jira Integration** | Communicates directly with Jira via Atlassian MCP servers to query issues and apply updates on the fly |
| 🖥️ **CLI-Driven Orchestration** | Suite of Bash scripts to execute operational modes or run automated cron schedules |
| 🏃 **Dry-Run by Default** | All modes default to dry-run; mutations only execute when `--apply --approved-by` are explicitly provided |
| 📝 **Audit Logging** | Every approval-gated run is logged with timestamp, authority, mode, and affected issue keys |

---

## 🗺️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Sprint Guardian                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CLI Entry Points (automation/*.sh)                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ shape-sprint │  │ triage-queue │  │suggest-owner │  ...     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         └─────────────────┴─────────────────┘                   │
│                           │                                      │
│                           ▼                                      │
│         ┌─────────────────────────────────┐                     │
│         │  run-sprint-guardian  │                     │
│         │  (Orchestrator)                 │                     │
│         │  • Loads team-map.local.yaml    │                     │
│         │  • Validates approval authority │                     │
│         │  • Assembles prompt context     │                     │
│         │  • Runs codex exec              │                     │
│         └────────────────┬────────────────┘                     │
│                          │                                       │
│           ┌──────────────┴──────────────┐                       │
│           │                             │                        │
│           ▼                             ▼                        │
│  ┌─────────────────┐       ┌────────────────────────┐           │
│  │  Codex / LLM    │       │   Atlassian MCP Server │           │
│  │  (AI Engine)    │◄─────►│   (Jira Read/Write)    │           │
│  └─────────────────┘       └────────────────────────┘           │
│                                                                  │
│  References & Config                                             │
│  ┌────────────────┐  ┌─────────────────┐  ┌──────────────────┐  │
│  │ team-map.yaml  │  │ ownership-policy│  │ jira-query-guide │  │
│  └────────────────┘  └─────────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧩 Operational Modes

| Mode | Script | Description |
|---|---|---|
| `shape-sprint` | `shape-sprint.sh` | Shapes sprint scope from backlog or board issues |
| `triage-queue` | `triage-queue.sh` | Classifies incoming backlog work and identifies next actions |
| `suggest-owner` | `suggest-owner.sh` | Recommends the best candidate to own specific issues |
| `balance-load` | `balance-load.sh` | Identifies overload and proposes safe owner reassignments |
| `inspect-sprint` | `inspect-sprint.sh` | Reviews sprint health, stale work, and bottlenecks |
| `surface-risk` | `surface-risk.sh` | Flags delivery risks before they become blockers |
| `progress-pulse` | `progress-pulse.sh` | Summarizes task movement and pending decisions |
| `standup-brief` | `standup-brief.sh` | Compiles daily sprint status updates for the team |
| `retro-notes` | `retro-notes.sh` | Prepares retrospective inputs from sprint patterns |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Core Logic** | LLM Prompt Engineering, System Skills (Markdown/YAML) |
| **AI Runtime** | Codex CLI (OpenAI / compatible LLM backend) |
| **Integration** | Model Context Protocol (MCP), Atlassian Jira API (JQL) |
| **Automation** | Bash / Shell Scripting |
| **Validation** | Python 3.8+, PyYAML |
| **Configuration** | YAML, Markdown templates |
| **Methodology** | Agile — Scrum & Sprint Management |

---

## 📋 Prerequisites

1. **Python 3.8+** — required for team map validation and authority checks
2. **Atlassian Jira MCP Server** — installed and running in your agent/assistant framework
3. **Codex CLI** — required to run automated shell commands and prompt execution

---

## 🚀 Quick Start

### Option A — Interactive Setup Wizard (Recommended)

Run the wizard to automatically generate `references/team-map.local.yaml` and `.env` in under 2 minutes:

```bash
./automation/setup.sh   # or: make setup
```

---

### Option B — Manual Configuration

#### Step 1 — Configure the Team Map

```bash
cp references/team-map.example.yaml references/team-map.local.yaml
```

Open `references/team-map.local.yaml` and configure:
- **Jira Board ID** and **Project Key**
- **Assigning Authorities** (who can approve Jira mutations)
- **Team Directory** (engineers, skills, capacity, WIP limits)

#### Step 2 — Set Up Environment

```bash
# Copy and fill in your environment variables
cp .env.example .env

# Create the Python virtual environment (in parent directory)
python -m venv ../.venv-jira-tools
source ../.venv-jira-tools/bin/activate   # Windows: ../.venv-jira-tools/Scripts/activate
pip install -r requirements.txt
```

### Step 3 — Install the Skill

```bash
./automation/install-skill.sh
```

This symlinks the skill folder into `~/.codex/skills/`.

### Step 4 — Validate Configuration

```bash
./automation/validate-skill.sh
```

---

## 💻 Usage Examples

### Dry-Run (Read-Only)

```bash
# Inspect sprint health
./automation/inspect-sprint.sh --board-id 1234

# Triage backlog queue
./automation/triage-queue.sh --board-id 1234 --project-key PROJ

# Recommend an owner for a ticket
./automation/suggest-owner.sh --issue-keys "PROJ-101,PROJ-102"

# Shape next sprint scope
./automation/shape-sprint.sh --board-id 1234 --start-date 2026-11-01 --end-date 2026-11-14

# Surface delivery risks
./automation/surface-risk.sh --board-id 1234 --sprint-id 4567

# Generate standup brief
./automation/standup-brief.sh --board-id 1234
```

### Apply Mode (Requires Human Approval)

```bash
# Suggest and apply an owner change (requires approved-by)
./automation/suggest-owner.sh \
  --issue-keys "PROJ-101" \
  --apply \
  --approved-by "Coder Coder"

# Balance workload and apply reassignments
./automation/balance-load.sh \
  --board-id 1234 \
  --apply \
  --approved-by "Coder Coder" \
  --approval-note "Sprint 42 rebalancing approved in standup"
```

### Debug Mode

```bash
# Enable shell trace for troubleshooting
./automation/run-sprint-guardian.sh --mode triage-queue --board-id 1234 --debug
```

---

## 🧪 Testing & Quality Assurance

Run the automated test suite to verify prompt schemas, shell syntax, permissions, and team map validator logic:

```bash
# Run tests with Python
python3 tests/run_tests.py

# Or via Makefile
make test
```

The test suite covers:
- **`test_validate_team_map.py`**: Team map schema validation, duplicate assignee detection, WIP bounds checking.
- **`test_prompts.py`**: Verifies all 9 prompt files exist, contain required behavior/output sections, and enforce approval-gating on mutation modes.
- **`test_shell_scripts.py`**: Ensures all automation wrappers pass `bash -n` syntax checks and retain executable (`+x`) permissions.

---

## ⚙️ Configuration Reference

### Environment Variables (`.env`)

| Variable | Description | Default |
|---|---|---|
| `SPRINT_ASSIGNER_BOARD_ID` | Default Jira board ID | _(required)_ |
| `SPRINT_ASSIGNER_PROJECT_KEYS` | Default Jira project key(s) | `PROJ` |
| `SPRINT_ASSIGNER_TEAM_MAP` | Path to team map YAML | `references/team-map.local.yaml` |
| `SPRINT_ASSIGNER_APPROVED_BY` | Default approval authority name | _(empty)_ |
| `SPRINT_ASSIGNER_SPRINT_ID` | Default sprint ID | _(empty)_ |
| `CODEX_MODEL` | Codex model override | _(codex default)_ |
| `CODEX_WORKDIR` | Working directory for codex exec | _(current dir)_ |

### Team Map Fields (`team-map.local.yaml`)

See [`references/team-map.example.yaml`](references/team-map.example.yaml) for the full schema.

---

## 🔒 Security & Governance

- **Dry-run by default**: No Jira mutations happen unless `--apply` is explicitly passed.
- **Human approval gate**: Any assignee change requires `--approved-by` matching a configured `assigning_authority` in the team map.
- **Authority validation**: The orchestrator runs a Python script to verify the `approved-by` value against the team map before executing.
- **Audit log**: All approved runs are logged to `automation/output/approvals.log` with timestamp, mode, authority, and affected issues.
- **Prompt injection protection**: Jira issue text, comments, and operator-supplied free text are treated as data — they cannot override skill guardrails.

---

## 📁 Project Structure

```
sprint-guardian/
├── SKILL.md                          # Core skill definition (loaded by Codex/Claude)
├── README.md                         # This file
├── CHANGELOG.md                      # Version history (SemVer)
├── Makefile                          # Developer command shortcuts (make test, etc.)
├── .env.example                      # Environment variable template
├── requirements.txt                  # Python dependencies (pyyaml)
├── .gitattributes                    # Enforce Unix LF line endings
├── .gitignore                        # Protect logs, local config, and caches
├── .github/
│   └── workflows/ci.yml              # GitHub Actions CI matrix test workflow
├── agents/
│   ├── openai.yaml                   # Codex / OpenAI agent interface config
│   └── claude-desktop-mcp.example.json # Claude Desktop Atlassian MCP config
├── automation/
│   ├── setup.sh            # Interactive setup CLI wrapper
│   ├── run-sprint-guardian.sh  # Main orchestrator
│   ├── shape-sprint.sh
│   ├── triage-queue.sh
│   ├── suggest-owner.sh
│   ├── balance-load.sh
│   ├── inspect-sprint.sh
│   ├── surface-risk.sh
│   ├── progress-pulse.sh
│   ├── standup-brief.sh
│   ├── retro-notes.sh
│   ├── install-skill.sh
│   ├── validate-skill.sh
│   ├── cron.example                  # Example cron schedules
│   ├── output/                       # Auto-generated run outputs (git-ignored)
│   └── prompts/                      # Mode-specific LLM prompt templates
│       ├── shape-sprint.md
│       ├── triage-queue.md
│       ├── suggest-owner.md
│       ├── balance-load.md
│       ├── inspect-sprint.md
│       ├── surface-risk.md
│       ├── progress-pulse.md
│       ├── standup-brief.md
│       └── retro-notes.md
├── scripts/
│   ├── setup_wizard.py               # Interactive terminal onboarding wizard
│   ├── validate_team_map.py          # Team map schema validator
│   └── check_env.py                  # Environment readiness checker
├── tests/
│   ├── run_tests.py                  # Unified test runner
│   ├── test_validate_team_map.py     # Team map validation unit tests
│   ├── test_prompts.py               # Prompt structure & approval tests
│   ├── test_shell_scripts.py         # Shell syntax & permission tests
│   └── fixtures/
│       └── mock_jira_issues.json     # Mock Jira test payload
├── references/
│   ├── team-map.example.yaml         # Team map schema example
│   ├── jira-query-guide.md           # JQL query reference
│   └── ownership-policy.md          # Owner scoring and approval rules
└── docs/
    ├── modes.md                      # Detailed mode documentation
    └── governance.md                 # Approval gate and audit log guide
```

---

## 🚢 Production Deployment

Sprint Guardian supports multiple production deployment strategies:

- 🐳 **Docker & Docker Compose**: Run scheduled cron daemons or one-off tasks in isolated containers.
- 🖥️ **Linux / macOS Server**: Deploy via automated system crontab (`make cron-install`).
- ⚡ **Serverless GitHub Actions**: Automate standup briefs and sprint reviews on schedule via [GitHub Actions](../.github/workflows/scheduled-sprint-guardian.yml) with zero server infrastructure.
- 💻 **Scrum Master CLI**: Direct execution via Codex CLI or Claude Code.

📖 **Full Deployment Guide**: See [**`docs/deployment.md`**](docs/deployment.md) for step-by-step production setup, Docker commands, and security checklists.

```bash
# Docker quick start
docker compose up -d sprint-guardian

# Server cron quick start
make cron-install
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes following [Conventional Commits](https://www.conventionalcommits.org/)
4. Open a pull request

---

