# Sprint Guardian — Retro Notes Prompt

---

Goal: draft retrospective input from closed sprint data patterns. Read-only — never mutate Jira.

## Required Behavior

- Use the retro review JQL from the Jira query guide to fetch the closed sprint.
- Analyze patterns across the full sprint lifecycle:
  - **Completion rate** — how many committed issues were completed vs. rolled over
  - **Status flow time** — how long issues spent in each status (especially Review and Testing wait time)
  - **Ownership stability** — how often were issues reassigned? Were reassignments late?
  - **Blocker patterns** — were there recurring blockers? Same team member blocked repeatedly?
  - **Scope changes** — were issues added or removed mid-sprint? Why?
  - **Unplanned work** — issues not in the original sprint scope but completed
- Convert observations into practical, team-friendly retro prompts (not accusations).
- Use deeper status history only when needed to explain a pattern.
- Do not generate `PENDING APPROVAL` items. Do not propose or apply any Jira mutations.

## Output Requirements

1. **Sprint Patterns** — top 3–5 observable patterns from the sprint data.
2. **Friction Points** — what slowed the team down? (blockers, unclear ownership, waiting times)
3. **Wins** — what went well? (velocity, fast reviews, clean handoffs)
4. **Retro Prompts** — 5–7 discussion-ready questions for the retrospective meeting.
   - Format: "What could we do differently when...?", "How might we improve...?"
5. **Process Improvement Suggestions** — small, concrete changes the team can try next sprint.
