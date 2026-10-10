#!/usr/bin/env python3
"""setup_wizard.py — Interactive configuration wizard for Sprint Guardian.

Generates:
  - references/team-map.local.yaml
  - .env

Usage:
  python3 scripts/setup_wizard.py [--non-interactive]
"""
from __future__ import annotations

import os
import sys

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF_DIR = os.path.join(ROOT_DIR, "references")
LOCAL_TEAM_MAP = os.path.join(REF_DIR, "team-map.local.yaml")
LOCAL_ENV = os.path.join(ROOT_DIR, ".env")


def prompt_str(label: str, default: str = "") -> str:
    default_hint = f" [{default}]" if default else ""
    try:
        val = input(f"{label}{default_hint}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        sys.exit(1)
    return val if val else default


def prompt_int(label: str, default: int) -> int:
    while True:
        raw = prompt_str(label, str(default))
        try:
            val = int(raw)
            if val > 0:
                return val
            print("  Please enter a positive integer.")
        except ValueError:
            print("  Please enter a valid integer.")


def prompt_csv(label: str, default: list[str]) -> list[str]:
    raw = prompt_str(label, ", ".join(default))
    return [item.strip() for item in raw.split(",") if item.strip()]


def run_wizard() -> None:
    print()
    print("======================================================")
    print("   🛡️  Sprint Guardian — Setup Wizard")
    print("======================================================")
    print("This wizard helps you configure your Jira board, team,")
    print("and approval authorities in under 2 minutes.")
    print()

    # Step 1: Jira Board Configuration
    print("--- 1. Jira Board & Project ---")
    board_id = prompt_str("Jira Board ID (numeric or string)", "1234")
    project_key = prompt_str("Default Jira Project Key", "PROJ")
    project_keys = [project_key]

    # Step 2: Assigning Authority
    print("\n--- 2. Assigning Authority (Human in the Loop) ---")
    print("Who has authority to approve Jira assignee mutations?")
    lead_name = prompt_str("Team Lead / Authority Name", "Team Lead")
    lead_email = prompt_str("Team Lead Jira Email / Username", "lead@example.com")

    # Step 3: Team Directory
    print("\n--- 3. Team Directory ---")
    print(f"Adding team lead '{lead_name}' to team roster...")
    lead_skills = prompt_csv(f"Skills for {lead_name}", ["backend", "lead", "automation"])
    lead_capacity = prompt_int(f"Sprint capacity points for {lead_name}", 15)
    lead_wip = prompt_int(f"Max in-progress WIP limit for {lead_name}", 3)

    team = [
        {
            "name": lead_name,
            "jira_assignee": lead_email,
            "team": project_key,
            "skills": lead_skills,
            "components": [project_key],
            "labels": [project_key.lower()],
            "max_in_progress": lead_wip,
            "sprint_capacity_points": lead_capacity,
            "backup_assignee": "",
            "unavailable_dates": [],
            "assignment_allowlist": True,
        }
    ]

    print("\nAdd team engineers:")
    while True:
        add_more = prompt_str("Add another engineer? (y/n)", "n").lower()
        if add_more not in ("y", "yes"):
            break
        eng_name = prompt_str("Engineer Name")
        if not eng_name:
            continue
        eng_email = prompt_str(f"Jira Email/ID for {eng_name}")
        eng_skills = prompt_csv(f"Skills for {eng_name}", ["frontend", "testing"])
        eng_capacity = prompt_int(f"Sprint capacity points for {eng_name}", 8)
        eng_wip = prompt_int(f"Max in-progress WIP for {eng_name}", 2)

        team.append({
            "name": eng_name,
            "jira_assignee": eng_email,
            "team": project_key,
            "skills": eng_skills,
            "components": [project_key],
            "labels": [project_key.lower()],
            "max_in_progress": eng_wip,
            "sprint_capacity_points": eng_capacity,
            "backup_assignee": lead_email,
            "unavailable_dates": [],
            "assignment_allowlist": True,
        })

    # Assemble team-map.local.yaml
    team_map_data = {
        "board": {
            "id": board_id,
            "project_keys": project_keys,
        },
        "defaults": {
            "dry_run": True,
            "backlog_jql": f"project in ({project_key}) AND statusCategory != Done AND sprint is EMPTY ORDER BY priority DESC, created ASC",
            "active_sprint_jql": f"project in ({project_key}) AND sprint in openSprints() ORDER BY Rank ASC",
            "fields": "summary,status,assignee,priority,components,labels,updated,created,duedate",
            "stale_after_days": 3,
            "standup_lookback_days": 1,
            "blocked_statuses": ["Blocked", "On Hold"],
            "active_statuses": ["In Progress", "In Review", "Testing"],
            "done_statuses": ["Done", "Closed", "Resolved"],
        },
        "approval": {
            "assignee_change_requires_approval": True,
            "allow_apply_without_approval": False,
            "assigning_authorities": [
                {
                    "name": lead_name,
                    "jira_assignee": lead_email,
                    "scope": project_keys,
                }
            ],
            "audit_log": "automation/output/approvals.log",
        },
        "team": team,
        "rules": {
            "ownership_order": ["component", "label", "skill", "history"],
            "never_auto_assign_labels": ["security", "architecture", "needs-manager-review"],
            "cross_team_assignment_requires_approval": True,
        },
    }

    # Step 4: Write team-map.local.yaml
    print(f"\nWriting {LOCAL_TEAM_MAP}...")
    with open(LOCAL_TEAM_MAP, "w", encoding="utf-8") as fh:
        yaml.dump(team_map_data, fh, sort_keys=False, default_flow_style=False)
    print("  ✅ Created references/team-map.local.yaml")

    # Step 5: Write .env
    print(f"Writing {LOCAL_ENV}...")
    env_content = f"""# Sprint Guardian — Local Environment
SPRINT_ASSIGNER_BOARD_ID={board_id}
SPRINT_ASSIGNER_PROJECT_KEYS={project_key}
SPRINT_ASSIGNER_TEAM_MAP=references/team-map.local.yaml
SPRINT_ASSIGNER_APPROVED_BY={lead_name}
"""
    with open(LOCAL_ENV, "w", encoding="utf-8") as fh:
        fh.write(env_content)
    print("  ✅ Created .env")

    print("\n======================================================")
    print("   🎉 Configuration Complete!")
    print("======================================================")
    print("Next steps:")
    print("  1. Validate setup:    ./automation/validate-skill.sh")
    print("  2. Test sprint check: ./automation/inspect-sprint.sh")
    print("  3. Run daily standup: ./automation/standup-brief.sh")
    print()


if __name__ == "__main__":
    run_wizard()
