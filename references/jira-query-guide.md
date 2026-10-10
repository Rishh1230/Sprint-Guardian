# Jira Query Guide

These examples use `PROJ` as the Jira project key. Adjust to match your project key.

Active sprint:

```text
project in (PROJ) AND sprint in openSprints() ORDER BY Rank ASC
```

Future sprint candidates:

```text
project in (PROJ) AND statusCategory != Done AND sprint is EMPTY ORDER BY priority DESC, created ASC
```

Backlog triage:

```text
project in (PROJ) AND statusCategory != Done AND sprint is EMPTY ORDER BY priority DESC, updated ASC
```

Unassigned work:

```text
project in (PROJ) AND assignee is EMPTY AND statusCategory != Done ORDER BY priority DESC, updated ASC
```

Stale work:

```text
project in (PROJ) AND statusCategory != Done AND updated <= -3d ORDER BY updated ASC
```

> **Note:** The `-3d` threshold mirrors `stale_after_days: 3` in `references/team-map.local.yaml`. If you change `stale_after_days`, update this query to match.

Delivery risk:

```text
project in (PROJ) AND statusCategory != Done AND (assignee is EMPTY OR updated <= -3d OR status in ("Blocked", "On Hold", "In Review", "Testing")) ORDER BY priority DESC, updated ASC
```

Workload balance:

```text
project in (PROJ) AND sprint in openSprints() AND statusCategory != Done ORDER BY assignee ASC, priority DESC
```

Daily pulse:

```text
project in (PROJ) AND sprint in openSprints() AND updated >= -1d ORDER BY updated DESC
```

Retro review:

```text
project in (PROJ) AND sprint in closedSprints() ORDER BY updated DESC
```

Suggested fields:

```text
summary,status,assignee,priority,components,labels,updated,created,duedate
```

Use `*all` only when a custom field is required and the field ID is unknown.
