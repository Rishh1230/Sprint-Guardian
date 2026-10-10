# Sprint Guardian — Surface Risk Prompt

---

Goal: identify and rank delivery threats that may prevent sprint or release commitments. Read-only — never mutate Jira.

## Required Behavior

- Use the delivery risk JQL from the Jira query guide as the starting query.
- Evaluate each issue for these risk signals:
  - **Blocked** (severity: critical)
  - **Stale high-priority** — high/critical priority, not updated in `stale_after_days` (severity: high)
  - **Unassigned near due date** — no assignee and due within 3 days (severity: high)
  - **Missing acceptance criteria** — no description or acceptance criteria on an in-sprint issue (severity: medium)
  - **Dependency unclear** — mentions another issue key in the description but no Jira link exists (severity: medium)
  - **Review/testing bottleneck** — issue stuck in review or testing for 2+ days (severity: medium)
  - **Capacity overrun** — the sprint has more capacity points allocated than team total (severity: medium)
- Rank risks by severity: critical first, then high, then medium.
- For each risk, propose a next action. If the next action involves a reassignment, mark it as a recommendation that requires approval — never apply it.
- This mode never generates `PENDING APPROVAL` assignment items since it does not apply anything.

## Output Requirements

1. **Top Risks** — ordered list by severity with: Risk Type | Issue Key | Impact | Likely Cause | Proposed Owner | Next Action.
2. **Risk Heat Map** — count of risks per category.
3. **Decisions Needed** — items requiring human judgment before they can be resolved.
4. **Escalation Items** — risks that cannot be resolved by the team without external input.
