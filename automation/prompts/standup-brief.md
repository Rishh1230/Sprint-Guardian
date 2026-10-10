# Sprint Guardian — Standup Brief Prompt

---

Goal: compile a concise, human-readable daily standup brief for the whole team. Read-only — never mutate Jira.

## Required Behavior

- Use the standup lookback period from `defaults.standup_lookback_days` (default: 1 day).
- Fetch recently updated issues and group them by assignee and status.
- Structure output as a team-level view first, then per-person summaries.
- Highlight blockers and stuck work prominently.
- Note any pending approvals that may be holding up team progress.
- Keep it brief. This is meant to be read aloud in a 15-minute standup. Avoid long descriptions — use bullet points.
- Do not generate `PENDING APPROVAL` items. Do not propose Jira mutations.

## Output Requirements

1. **Team Summary** — 2–3 sentence overview of where the sprint stands today.
2. **Done (last 24 hours)** — issues completed since yesterday.
3. **In Progress** — active issues with owner names.
4. **Blockers & Stuck Items** — anything blocked, stale, or needing a decision right now.
5. **Stale Tickets** — tickets with no update in more than `stale_after_days`.
6. **Pending Approvals** — outstanding approval items from previous runs.
7. **Today's Focus** — one-line suggestion for what the team should prioritize today.
