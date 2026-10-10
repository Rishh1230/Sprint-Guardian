# Sprint Guardian — Balance Load Prompt

---

Goal: identify developers who are overloaded in the active sprint and propose safe, policy-compliant reassignments.

## Required Behavior

- Fetch all active sprint issues using the workload balance JQL from the Jira query guide.
- For each team member in the team map, compute:
  - Current in-progress issue count vs `max_in_progress` WIP limit
  - Current sprint capacity points used vs `sprint_capacity_points`
  - Number of blocked issues assigned to them
- Identify overloaded members (at or above WIP limit OR above capacity).
- Identify underloaded members (below WIP limit AND have remaining capacity).
- Propose reassignments only from overloaded to underloaded members.
- Score every proposed move using the ownership policy. Do not propose cross-team moves without a routing rule.
- Never propose reassignments for issues labeled `security`, `architecture`, or `needs-manager-review`.
- All reassignments require explicit human approval. In dry-run mode, everything is `PENDING APPROVAL`.
- In apply mode with `approved-by`, apply only medium or high confidence moves with no hard blocker.

## Output Requirements

1. **Load Summary** — table: Team Member | In-Progress | WIP Limit | Capacity Used | Capacity Total | Status.
2. **Overloaded Members** — who is over limit and by how much.
3. **Proposed Reassignments** — for each proposed move: Issue Key | From | To | Confidence | Reason | Risk.
4. **Assignment Approval Items** — `PENDING APPROVAL` format for every proposed reassignment.
5. **Applied Changes** — only when `approved-by` was present.
6. **Missing Inputs or Risks** — team members not in team map, missing capacity data.
