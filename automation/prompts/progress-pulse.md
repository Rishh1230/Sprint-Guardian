# Sprint Guardian — Progress Pulse Prompt

---

Goal: produce a concise, data-driven sprint progress snapshot. Read-only — never mutate Jira.

## Required Behavior

- Use the daily pulse JQL from the Jira query guide to fetch recently updated issues.
- If a previous snapshot file is included in the run context, compare current state against it to highlight movement.
- Track:
  - Issues moved to Done since the last snapshot
  - Issues that changed status (e.g. moved from In Progress to Review)
  - Issues that have not moved since the last snapshot (stale)
  - New issues added to the sprint since the last snapshot
  - Pending approvals still outstanding
- Keep the summary concise — this is a pulse check, not a full health report. Use `inspect-sprint` for deep dives.
- Do not generate `PENDING APPROVAL` items. Do not propose Jira mutations.

## Output Requirements

1. **Movement Since Last Snapshot** — table: Issue Key | From Status | To Status | Assignee.
2. **Completed Since Last Run** — issues moved to Done.
3. **Stale / No Movement** — issues that have not changed since the last snapshot.
4. **Sprint Velocity Trend** — simple comparison: done count now vs. last snapshot.
5. **Pending Decisions** — anything still waiting for human action (approvals, unblocking).
6. **Next Check-in Suggestion** — brief note on what to focus on before the next pulse run.
