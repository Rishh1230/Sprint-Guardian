# Sprint Guardian — Triage Queue Prompt

---

Goal: classify backlog or queue work systematically and surface what needs immediate attention.

## Required Behavior

- Fetch the backlog using the supplied JQL or `defaults.backlog_jql` from the team map.
- Classify each issue using exactly one of these labels:
  - `ready` — has owner, description, acceptance criteria, unblocked dependencies
  - `sprint-candidate` — ready AND high priority AND fits capacity
  - `unclear` — missing description, acceptance criteria, or ambiguous scope
  - `blocked` — has a dependency blocker or is in a blocked status
  - `duplicate/link-needed` — likely duplicate or missing a Jira link to parent/related issue
  - `owner-needed` — unassigned and otherwise ready to assign
- Highlight issues that have been sitting in backlog without movement for more than `defaults.stale_after_days`.
- Owner recommendations must follow the ownership policy. Applying owner changes requires explicit human approval.
- In apply mode, non-assignee actions (labels, comments, watchers) may be proposed; assignee changes still require `approved-by`.

## Output Requirements

1. **Queue Health Summary** — count per classification, overall assessment (healthy / needs attention / critical).
2. **Sprint Candidates** — ordered list of the most sprint-ready issues.
3. **Owner-Needed Issues** — issues without an owner that are otherwise ready; include a recommended owner scored per ownership policy.
4. **Blocked & Unclear Issues** — what is blocking each issue and the suggested next action to unblock.
5. **Stale Issues** — issues unchanged for more than the configured stale threshold.
6. **Assignment Approval Items** — `PENDING APPROVAL` format for every owner recommendation.
7. **Next Triage Actions** — three to five concrete actions the team lead should take today.
