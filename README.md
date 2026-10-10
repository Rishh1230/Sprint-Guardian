# Sprint Guardian

Sprint Guardian is an Agile sprint coordination tool that integrates with Jira through the Model Context Protocol (MCP). It automates backlog triage, workload balancing across team members, sprint health inspections, risk analysis, and daily standup preparation, while keeping all ticket mutations behind an explicit human approval gate.

---

## Key Capabilities

- **Workload Balancing**: Evaluates active sprint allocation against defined developer capacities and Work-In-Progress (WIP) limits, recommending reassignments when imbalance occurs.
- **Approval-Gated Writes**: Defaults to read-only operation. Reassignments and issue mutations require an authorized operator identifier (`--approved-by`) matching the team configuration.
- **Sprint Analysis**: Inspects active sprints for blocked items, stale tickets, review bottlenecks, and unassigned in-progress work.
- **Ceremony Automation**: Generates structured summaries for daily standups, sprint shaping proposals, queue triage notes, and retrospectives.
- **Audit Trail**: Records every approved write action with timestamp, approving authority, affected issue keys, and output artifact paths.

---

## Architecture Overview

```
                          CLI / Scheduled Runners
                     (automation/*.sh / cron / Docker)
                                     │
                                     ▼
                      ┌──────────────────────────────┐
                      │    run-sprint-guardian.sh    │
                      │  - Loads local team map      │
                      │  - Verifies approval auth    │
                      │  - Builds mode context       │
                      │  - Executes Codex runtime    │
                      └──────────────┬───────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
         ┌─────────────────────┐           ┌─────────────────────┐
         │    Codex Engine     │◄─────────►│  Atlassian Jira MCP │
         │ (Prompt Evaluation) │           │    (Read / Write)   │
         └─────────────────────┘           └─────────────────────┘
```

---

## Operational Modes

| Mode | Entry Script | Description | Mutation Support |
|---|---|---|---|
| `shape-sprint` | `automation/shape-sprint.sh` | Build sprint proposals based on priority and team capacity | Optional (Scope / Assignee) |
| `triage-queue` | `automation/triage-queue.sh` | Classify backlog work and highlight missing specifications | Optional (Labels / Comments) |
| `suggest-owner` | `automation/suggest-owner.sh` | Score and recommend candidate assignees for specific issues | Optional (Assignee) |
| `balance-load` | `automation/balance-load.sh` | Identify overloaded developers and propose reassignments | Optional (Assignee) |
| `inspect-sprint` | `automation/inspect-sprint.sh` | Review sprint health, stuck items, and bottlenecks | Read-only |
| `surface-risk` | `automation/surface-risk.sh` | Detect delivery risks before they become blockers | Read-only |
| `progress-pulse` | `automation/progress-pulse.sh` | Summarize task transitions and velocity since last run | Read-only |
| `standup-brief` | `automation/standup-brief.sh` | Compile daily team status summary | Read-only |
| `retro-notes` | `automation/retro-notes.sh` | Extract patterns and discussion points from closed sprints | Read-only |

---

## Prerequisites

1. **Python 3.8+** (standard library plus `pyyaml`)
2. **Atlassian Jira MCP Server** (configured in your local assistant or agent environment)
3. **Codex CLI** (for prompt evaluation and workflow execution)

---

## Quick Start

### 1. Interactive Setup

Run the configuration wizard to generate `references/team-map.local.yaml` and `.env`:

```bash
./automation/setup.sh
# or: make setup
```

### 2. Manual Configuration (Alternative)

Copy the reference templates directly:

```bash
cp references/team-map.example.yaml references/team-map.local.yaml
cp .env.example .env
```

Edit `references/team-map.local.yaml` with your board ID, project key, team directory, and assigned approval authorities.

### 3. Install Dependencies & Verify Environment

```bash
pip install -r requirements.txt

# Run automated validation and test suite
make test
make check-env
```

### 4. Install Skill to Agent Directory

```bash
./automation/install-skill.sh
# Links to ~/.codex/skills/ and ~/.claude/skills/ if present
```

---

## Usage Examples

### Read-Only Invocations

All scripts default to dry-run mode and will not mutate Jira tickets.

```bash
# Generate daily standup summary
./automation/standup-brief.sh --board-id 1234

# Inspect sprint health and bottlenecks
./automation/inspect-sprint.sh --board-id 1234 --sprint-id 4567

# Triage incoming backlog items
./automation/triage-queue.sh --board-id 1234 --project-key PROJ

# Surface active delivery risks
./automation/surface-risk.sh --board-id 1234 --sprint-id 4567

# Recommend assignee for specific tickets (dry-run output)
./automation/suggest-owner.sh --issue-keys "PROJ-101,PROJ-102"
```

### Mutation Invocations (Requires Approval)

To apply changes to Jira, provide both `--apply` and `--approved-by`:

```bash
# Apply recommended owner with authorization
./automation/suggest-owner.sh \
  --issue-keys "PROJ-101" \
  --apply \
  --approved-by "Team Lead"

# Balance workload and write reassignments to Jira
./automation/balance-load.sh \
  --board-id 1234 \
  --apply \
  --approved-by "Team Lead" \
  --approval-note "Approved during sprint planning"
```

### Debugging

Enable shell execution trace using `--debug`:

```bash
./automation/run-sprint-guardian.sh --mode triage-queue --board-id 1234 --debug
```

---

## Testing

The test suite validates prompt integrity, team map schemas, shell syntax, and permission models.

```bash
python3 tests/run_tests.py
# or: make test
```

Test coverage includes:
- `test_validate_team_map.py`: Verifies schema requirements, WIP constraints, and prevents duplicate assignees.
- `test_prompts.py`: Confirms prompt section structures and approval-rule enforcement.
- `test_shell_scripts.py`: Validates syntax with `bash -n` and checks executable permissions.

---

## Configuration Reference

### Environment Variables (`.env`)

| Variable | Description | Default |
|---|---|---|
| `SPRINT_ASSIGNER_BOARD_ID` | Default Jira board identifier | Empty |
| `SPRINT_ASSIGNER_PROJECT_KEYS` | Comma-separated Jira project keys | `PROJ` |
| `SPRINT_ASSIGNER_TEAM_MAP` | Path to active team map configuration | `references/team-map.local.yaml` |
| `SPRINT_ASSIGNER_APPROVED_BY` | Default approval authority name | Empty |
| `SPRINT_ASSIGNER_SPRINT_ID` | Default sprint identifier | Empty |
| `CODEX_MODEL` | Codex model override | Default model |
| `CODEX_WORKDIR` | Working directory for codex execution | Current directory |

---

## Production Deployment

Refer to [`docs/deployment.md`](docs/deployment.md) for full deployment documentation.

Supported deployment targets:
- **Docker / Docker Compose**: Run scheduled cron background daemons or on-demand CLI tasks.
- **Server Crontab**: Install automated schedules directly via `make cron-install`.
- **GitHub Actions**: Run automated ceremonies via scheduled workflows without standing infrastructure.
- **Local Developer CLI**: Direct execution by Scrum Masters and engineering leads.

---

## Repository Structure

```
sprint-guardian/
├── SKILL.md                          # Core agent skill definition
├── README.md                         # Technical documentation
├── CHANGELOG.md                      # Release history
├── Makefile                          # Common development targets
├── Dockerfile                        # Container image definition
├── docker-compose.yml                # Containerized daemon service
├── LICENSE                           # MIT License
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variable template
├── .gitignore                        # Git exclusion rules
├── .gitattributes                    # Line ending normalization
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Automated CI test matrix
│       └── scheduled-sprint-guardian.yml # Scheduled cloud workflows
├── agents/
│   ├── openai.yaml                   # Codex agent interface configuration
│   └── claude-desktop-mcp.example.json # Claude Desktop MCP configuration
├── automation/
│   ├── setup.sh                      # Setup wizard launcher
│   ├── run-sprint-guardian.sh        # Primary orchestrator
│   ├── *.sh                          # Mode-specific wrapper scripts
│   ├── cron.example                  # Reference crontab configurations
│   └── prompts/*.md                  # Operational prompt templates
├── docs/
│   ├── deployment.md                 # Deployment and infrastructure guide
│   ├── governance.md                 # Approval model and security specifications
│   └── modes.md                      # Operational modes reference
├── references/
│   ├── team-map.example.yaml         # Team map schema example
│   ├── jira-query-guide.md           # JQL query reference
│   └── ownership-policy.md          # Scoring policy and approval rules
├── scripts/
│   ├── setup_wizard.py               # Interactive onboarding wizard
│   ├── validate_team_map.py          # Team map validator
│   ├── check_env.py                  # Environment readiness checker
│   ├── verify_mcp_connection.py      # Jira API connectivity verifier
│   ├── install_cron.sh               # Crontab installer
│   └── docker-entrypoint.sh          # Container entrypoint
└── tests/
    ├── run_tests.py                  # Test suite runner
    ├── test_validate_team_map.py     # Team map unit tests
    ├── test_prompts.py               # Prompt structure tests
    ├── test_shell_scripts.py         # Shell syntax tests
    └── fixtures/
        └── mock_jira_issues.json     # Mock test fixtures
```
