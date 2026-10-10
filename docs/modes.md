# Sprint Guardian — Operational Modes Reference

Detailed documentation for all 9 operational modes of Sprint Guardian.

---

## Mode Overview

| Mode | Mutation Support | Approval Required? | Jira Writes |
|---|---|---|---|
| `shape-sprint` | Supported | Yes (for assignee changes) | Sprint scope, issue moves |
| `triage-queue` | Supported | Yes (for assignee changes) | Labels, comments, watchers |
| `suggest-owner` | Supported | Yes (always) | Assignee field |
| `balance-load` | Supported | Yes (always) | Assignee field |
| `inspect-sprint` | None (Read-only) | N/A | None |
| `surface-risk` | None (Read-only) | N/A | None |
| `progress-pulse` | None (Read-only) | N/A | None |
| `standup-brief` | None (Read-only) | N/A | None |
| `retro-notes` | None (Read-only) | N/A | None |

---

## 1. `shape-sprint`

**Purpose:** Build a proposed sprint scope from backlog or board issues.

**What it does:**
- Checks for active or future sprints before proposing changes
- Uses supplied JQL or the configured backlog query
- Prioritizes ready work with clear ownership and manageable capacity impact
- Avoids blocked or ownerless issues unless explicitly requested
- Produces a ranked list of: Selected, Deferred, and Risky issues

**Input options:**
```bash
./automation/shape-sprint.sh \
  --board-id 1234 \
  --project-key PROJ \
  --start-date 2026-11-01 \
  --end-date 2026-11-14
```

**Output sections:**
1. Sprint Scope Decision
2. Selected Issues (with capacity estimate)
3. Deferred Issues (with reason)
4. Risky Issues
5. Assignment Approval Items
6. Recommended Jira Actions

---

## 2. `triage-queue`

**Purpose:** Classify backlog or queue work and identify what needs attention.

**Classifications:**
- `ready` — has owner, description, acceptance criteria
- `sprint-candidate` — high priority, ready, fits capacity
- `unclear` — missing description or acceptance criteria
- `blocked` — depends on unresolved work
- `duplicate/link-needed` — likely duplicate or missing link
- `owner-needed` — unassigned and ready to assign

**Input options:**
```bash
./automation/triage-queue.sh \
  --board-id 1234 \
  --jql "project = PROJ AND sprint is EMPTY ORDER BY priority DESC"
```

---

## 3. `suggest-owner`

**Purpose:** Recommend the best assignee for specific issues using the ownership scoring model.

**Scoring considers:**
- Component ownership (+4), Label ownership (+3), Skill match (+3)
- Recent similar work (+2), Watcher/reviewer activity (+2)
- WIP limit headroom, sprint capacity, availability

**Requires approval to apply.** Without `--approved-by`, all recommendations are `PENDING APPROVAL`.

```bash
# Dry-run: generate recommendations only
./automation/suggest-owner.sh --issue-keys "PROJ-101,PROJ-102"

# Apply: requires authorized approval
./automation/suggest-owner.sh \
  --issue-keys "PROJ-101" \
  --apply \
  --approved-by "Coder Coder"
```

---

## 4. `balance-load`

**Purpose:** Review workload distribution, find overloaded developers, and propose safe reassignments.

**What it checks:**
- Current active issue count per developer vs WIP limits
- Sprint capacity points used vs allocated
- Cross-team ownership risks

**Requires approval to apply any reassignment.**

```bash
./automation/balance-load.sh \
  --board-id 1234 \
  --apply \
  --approved-by "Coder Coder" \
  --approval-note "Approved in Sprint 42 standup"
```

---

## 5. `inspect-sprint`

**Purpose:** Review overall sprint health. Read-only — never mutates Jira.

**What it inspects:**
- Blocked issues and blockers
- Stale work (unchanged beyond `stale_after_days`)
- Unassigned in-progress issues
- Overdue issues
- Review-stuck and testing-stuck tickets
- Velocity indicators

```bash
./automation/inspect-sprint.sh --board-id 1234 --sprint-id 4567
```

---

## 6. `surface-risk`

**Purpose:** Flag delivery threats before they become sprint blockers. Read-only.

**Risk signals:**
- Blocked issues (high severity)
- Stale high-priority work
- Unassigned issues near due date
- Issues with unclear or missing acceptance criteria
- Review/testing bottlenecks
- Capacity overruns

**Output order:** Findings by severity → Owner/Proposed Owner → Next Action → Decisions Needed

```bash
./automation/surface-risk.sh --board-id 1234 --sprint-id 4567
```

---

## 7. `progress-pulse`

**Purpose:** Short status snapshot showing movement since the last run. Read-only.

**Includes:**
- Issues moved to Done since last snapshot
- Issues that changed status
- Stale or stuck issues
- Pending decisions and approvals
- Comparison with previous snapshot (auto-detected)

```bash
./automation/progress-pulse.sh --board-id 1234 --sprint-id 4567
```

---

## 8. `standup-brief`

**Purpose:** Compile a daily team standup summary. Read-only.

**Sections:**
- Done (last 24 hours)
- In Progress (active work)
- Blocked / Decisions Needed
- Stale Tickets
- Pending Approvals

```bash
./automation/standup-brief.sh --board-id 1234
```

---

## 9. `retro-notes`

**Purpose:** Draft retrospective input from closed sprint data. Read-only, never mutates Jira.

**Analyzes:**
- Completion rate and velocity
- Time-in-status patterns (review/testing wait times)
- Ownership changes and reassignment frequency
- Blocked issue patterns
- Process improvement opportunities

**Output:** Sprint patterns → Friction points → Wins → Retro prompts → Small process improvements

```bash
./automation/retro-notes.sh --board-id 1234 --sprint-id 4567
```

---

*[Back to README](../README.md)*
