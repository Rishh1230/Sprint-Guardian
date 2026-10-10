# Sprint Guardian — Shape Sprint Prompt

---

Goal: build a well-scoped, capacity-aware sprint proposal from Jira backlog or board issues.

## Required Behavior

- Inspect existing active or future sprints before proposing scope changes. If a sprint already has scope, show what is currently planned before recommending additions or removals.
- Use the supplied JQL or the `defaults.backlog_jql` from the team map. Never invent issues.
- Score each candidate issue using the Sprint Readiness Score from the ownership policy.
- Prefer: high-priority issues, issues with clear owners, issues with defined acceptance criteria, issues with unblocked dependencies.
- Avoid: blocked issues, ownerless high-complexity issues, issues with missing acceptance criteria — unless explicitly asked to include them.
- Track cumulative capacity points as you add issues; stop adding when the team's `sprint_capacity_points` total is reached.
- Keep owner recommendations as `PENDING APPROVAL` items unless `approved-by` is present in the run context.
- If apply mode is active without `approved-by`, sprint-scope mutations (adding issues to sprint) may proceed, but assignee changes must remain as approval items.

## Output Requirements

1. **Sprint Scope Decision** — one-paragraph summary of the proposed sprint focus and rationale.
2. **Selected Issues** — table with columns: Issue Key | Summary | Priority | Owner | Capacity Points | Reason Selected.
3. **Deferred Issues** — table with columns: Issue Key | Summary | Reason Deferred.
4. **Risky Issues** — issues included despite one or more risk signals; show the risk.
5. **Assignment Approval Items** — use `PENDING APPROVAL` format for all owner recommendations.
6. **Recommended Jira Actions** — list only when apply mode is active; separate sprint-scope actions from assignee actions.
7. **Missing Inputs or Risks** — unresolved blockers or data gaps that could affect the scope.
