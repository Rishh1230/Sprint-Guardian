#!/usr/bin/env python3
"""validate_team_map.py — Validates a Sprint Guardian team map YAML file.

Usage:
    python scripts/validate_team_map.py [path/to/team-map.yaml]

Exit codes:
    0 — valid
    1 — validation error
    2 — file not found or unreadable
"""
from __future__ import annotations

import sys
import os

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REQUIRED_BOARD_FIELDS = ["id", "project_keys"]
REQUIRED_TEAM_MEMBER_FIELDS = [
    "name",
    "jira_assignee",
    "skills",
    "max_in_progress",
    "sprint_capacity_points",
]
REQUIRED_AUTHORITY_FIELDS = ["name", "jira_assignee", "scope"]


def error(msg: str) -> None:
    print(f"[ERROR] {msg}", file=sys.stderr)


def warn(msg: str) -> None:
    print(f"[WARN]  {msg}")


def info(msg: str) -> None:
    print(f"[OK]    {msg}")


def validate(data: dict) -> list[str]:
    errors: list[str] = []

    # --- board section ---
    board = data.get("board")
    if not isinstance(board, dict):
        errors.append("Missing required top-level key: 'board'")
    else:
        for field in REQUIRED_BOARD_FIELDS:
            if not board.get(field):
                errors.append(f"board.{field} is missing or empty")
        keys = board.get("project_keys", [])
        if not isinstance(keys, list) or len(keys) == 0:
            errors.append("board.project_keys must be a non-empty list")

    # --- defaults section ---
    defaults = data.get("defaults")
    if not isinstance(defaults, dict):
        errors.append("Missing required top-level key: 'defaults'")
    else:
        for field in ["backlog_jql", "active_sprint_jql", "stale_after_days"]:
            if field not in defaults:
                warn(f"defaults.{field} is missing — will fall back to built-in default")

    # --- approval section ---
    approval = data.get("approval")
    if not isinstance(approval, dict):
        errors.append("Missing required top-level key: 'approval'")
    else:
        authorities = approval.get("assigning_authorities", [])
        if not isinstance(authorities, list) or len(authorities) == 0:
            errors.append("approval.assigning_authorities must be a non-empty list")
        else:
            for i, authority in enumerate(authorities):
                if not isinstance(authority, dict):
                    errors.append(f"approval.assigning_authorities[{i}] must be a mapping")
                    continue
                for field in REQUIRED_AUTHORITY_FIELDS:
                    if not authority.get(field):
                        errors.append(
                            f"approval.assigning_authorities[{i}].{field} is missing or empty"
                        )

    # --- team section ---
    team = data.get("team")
    if not isinstance(team, list) or len(team) == 0:
        errors.append("Missing or empty top-level key: 'team' (must be a non-empty list)")
    else:
        assignees: set[str] = set()
        for i, member in enumerate(team):
            if not isinstance(member, dict):
                errors.append(f"team[{i}] must be a mapping")
                continue
            for field in REQUIRED_TEAM_MEMBER_FIELDS:
                if field not in member or member[field] is None:
                    errors.append(f"team[{i}] ({member.get('name', '?')}).{field} is missing")
            # Type checks
            wip = member.get("max_in_progress")
            if wip is not None and (not isinstance(wip, int) or wip < 1):
                errors.append(
                    f"team[{i}] ({member.get('name')}).max_in_progress must be a positive integer"
                )
            capacity = member.get("sprint_capacity_points")
            if capacity is not None and (not isinstance(capacity, (int, float)) or capacity < 0):
                errors.append(
                    f"team[{i}] ({member.get('name')}).sprint_capacity_points must be >= 0"
                )
            # Check for duplicate assignees
            jira_id = member.get("jira_assignee", "")
            if jira_id in assignees:
                errors.append(
                    f"team[{i}]: jira_assignee '{jira_id}' appears more than once in the team"
                )
            elif jira_id:
                assignees.add(jira_id)

    # --- rules section ---
    rules = data.get("rules")
    if not isinstance(rules, dict):
        warn("'rules' section is missing — ownership ordering will use defaults")

    return errors


def main() -> None:
    team_map_path = sys.argv[1] if len(sys.argv) > 1 else "references/team-map.local.yaml"

    if not os.path.isfile(team_map_path):
        error(f"File not found: {team_map_path}")
        print()
        print("To create it, run:")
        print("  cp references/team-map.example.yaml references/team-map.local.yaml")
        sys.exit(2)

    with open(team_map_path, "r", encoding="utf-8") as fh:
        try:
            data = yaml.safe_load(fh) or {}
        except yaml.YAMLError as exc:
            error(f"YAML parse error in {team_map_path}: {exc}")
            sys.exit(1)

    print(f"Validating: {team_map_path}")
    print("-" * 50)

    errors = validate(data)

    if errors:
        for msg in errors:
            error(msg)
        print()
        print(f"Validation FAILED — {len(errors)} error(s) found.")
        sys.exit(1)
    else:
        team = data.get("team", [])
        board = data.get("board", {})
        info(f"Board ID: {board.get('id')} | Project keys: {board.get('project_keys')}")
        info(f"Team members: {len(team)}")
        authorities = (data.get("approval") or {}).get("assigning_authorities", [])
        info(f"Assigning authorities: {len(authorities)}")
        print()
        print("Validation PASSED [OK]")


if __name__ == "__main__":
    main()
