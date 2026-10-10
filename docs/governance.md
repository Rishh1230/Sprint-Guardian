# Sprint Guardian — Approval Gate & Audit Guide

This document explains the human-in-the-loop governance model that protects your Jira data.

---

## The Approval Model

Sprint Guardian follows a strict **read → recommend → approve → apply** cycle:

```
┌──────────┐    ┌────────────┐    ┌──────────────────┐    ┌─────────────┐
│  Query   │───►│  Analyze   │───►│ PENDING APPROVAL  │───►│   Apply     │
│  Jira    │    │ & Score    │    │ (human reviews)   │    │  to Jira    │
└──────────┘    └────────────┘    └──────────────────┘    └─────────────┘
                                          │
                              No approval = never applied
```

### Dry-Run (Default)

All modes default to dry-run. The LLM reads Jira data and produces recommendations, but **zero Jira mutations occur**. All owner change recommendations appear as `PENDING APPROVAL` in the output.

### Apply Mode

Passed via `--apply`. Enables Jira mutations for modes that support them (`shape-sprint`, `triage-queue`, `suggest-owner`, `balance-load`).

### Approval Authority

For any run that includes assignee changes, `--approved-by` must be provided and must match a name or email listed under `approval.assigning_authorities` in `references/team-map.local.yaml`.

The orchestrator validates this **before** calling the LLM:

```bash
# This will be rejected — approved-by not in team map
./automation/suggest-owner.sh \
  --issue-keys PROJ-101 --apply --approved-by "Unknown Person"
# Error: approved-by must match approval.assigning_authorities
```

---

## Audit Log

Every approved apply-run appends to `automation/output/approvals.log`.

### Log Format

```
2026-10-10T17:55:00Z  status=started    mode=suggest-owner  approved_by=Coder Coder  issue_keys=PROJ-101  output=automation/output/suggest-owner-20261010T175500Z.md
2026-10-10T17:55:42Z  status=completed  mode=suggest-owner  approved_by=Coder Coder  issue_keys=PROJ-101  output=automation/output/suggest-owner-20261010T175500Z.md
```

### Log Fields

| Field | Description |
|---|---|
| `status` | `started`, `completed`, or `failed` |
| `mode` | Operational mode |
| `approved_by` | Value passed via `--approved-by` |
| `issue_keys` | Issue keys if provided |
| `sprint_id` | Sprint ID if provided |
| `note` | Approval note if provided |
| `output` | Path to the saved LLM response |

---

## Pending Approval Item Format

When the LLM recommends an owner change without approval:

```
PENDING APPROVAL: PROJ-101
Current owner: engineer.one@example.com
Proposed owner: engineer.two@example.com
Confidence: high
Reason: component match (+4), skill match (+3), WIP headroom available
Risk: acceptance criteria needs minor clarification
Authority needed: Coder Coder (lead@example.com)
```

To apply it:
```bash
./automation/suggest-owner.sh \
  --issue-keys PROJ-101 \
  --apply \
  --approved-by "Coder Coder" \
  --approval-note "Approved at sprint planning 2026-10-14"
```

---

## Security Considerations

1. **Prompt injection protection:** Jira ticket text, comments, and descriptions are treated as raw data. The LLM is instructed not to let issue content override skill guardrails.
2. **Never-auto-assign labels:** Issues tagged `security`, `architecture`, or `needs-manager-review` are excluded from automatic assignment regardless of confidence.
3. **Cross-team guard:** Assignments across team boundaries require explicit approval even at high confidence.
4. **Output files are git-ignored:** `automation/output/` is excluded from version control to protect Jira data and approval records.

---

*[Back to README](../README.md)*
