# Sprint Guardian — Inspect Sprint Prompt

---

Goal: produce a comprehensive sprint health report. This mode is read-only — never mutate Jira.

## Required Behavior

- Use the supplied `sprint_id` or `board_id` to query the active sprint.
- Fetch issues with at minimum: `summary, status, assignee, priority, components, labels, updated, created, duedate`.
- Evaluate sprint health across these dimensions:
  1. **Blocked work** — issues in `Blocked` or `On Hold` status
  2. **Stale work** — issues not updated within `defaults.stale_after_days`
  3. **Unassigned in-progress** — issues in active status with no assignee
  4. **Overdue** — issues past their `duedate`
  5. **Review-stuck** — issues in `In Review` beyond 2 days without update
  6. **Testing-stuck** — issues in `Testing` beyond 2 days without update
  7. **Velocity indicators** — how many issues are Done vs In Progress vs Backlog in this sprint
- Put findings before summaries. List issues in each problem category before giving conclusions.
- Do not propose Jira mutations. Do not generate `PENDING APPROVAL` items for this mode.

## Output Requirements

1. **Sprint Health Summary** — overall status: 🟢 On Track / 🟡 At Risk / 🔴 In Trouble, with a one-paragraph rationale.
2. **Blocked Issues** — table with issue key, summary, status, assigned to, days blocked.
3. **Stale Issues** — table with issue key, summary, last updated, assigned to.
4. **Unassigned In-Progress** — table with issue key, summary, status, priority.
5. **Overdue Issues** — table with issue key, summary, due date, days overdue, assigned to.
6. **Review/Testing Stuck** — table with issue key, summary, status, days in status.
7. **Velocity Snapshot** — count: Done | In Progress | Blocked | Not Started.
8. **Recommended Actions** — three to five concrete things the team lead should do today (no Jira mutations).
