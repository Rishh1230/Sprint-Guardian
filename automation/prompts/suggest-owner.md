# Sprint Guardian — Suggest Owner Prompt

---

Goal: recommend the best owner for each supplied issue key; all owner changes require explicit human approval before Jira is mutated.

## Required Behavior

- Fetch each issue from Jira using the supplied `issue_keys`.
- For each issue, score every eligible team member using the ownership policy:
  - Apply all positive and negative signals
  - Compute a total score and a confidence rating (high / medium / low)
  - Identify the top candidate and the closest alternative
- Never recommend a team member who is at or above their WIP limit or unavailable in the sprint window.
- Never auto-assign issues labeled `security`, `architecture`, or `needs-manager-review`.
- Cross-team assignments always require explicit approval regardless of confidence level.
- In dry-run mode, all recommendations are `PENDING APPROVAL` — never update Jira.
- In apply mode, update Jira assignee only when `approved-by` is present AND confidence is medium or high AND no hard blocker exists.

## Scoring Output Per Issue

For each issue, show:

```
Issue: ISSUE-KEY — Issue Summary
Current owner: current.owner@example.com (or Unassigned)
Top candidate: proposed.owner@example.com
  Score: +7 (component +4, skill +3)
  Confidence: high
  WIP: 1 of 3 | Capacity: 6 of 15 pts
Alternative: backup.owner@example.com
  Score: +4 (label +3, backup +1)
  Confidence: medium
```

## Output Requirements

1. **Assignment Decision** — one-paragraph summary of recommendations and confidence.
2. **Issue-by-Issue Scoring** — full scoring block per issue as shown above.
3. **Assignment Approval Items** — `PENDING APPROVAL` format for every proposed change.
4. **Applied Changes** — only when `approved-by` was present; list Jira actions taken.
5. **Missing Inputs or Blockers** — data gaps that prevented a confident recommendation.
