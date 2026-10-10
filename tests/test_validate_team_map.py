#!/usr/bin/env python3
"""test_validate_team_map.py — Unit tests for team map validation logic."""
from __future__ import annotations

import os
import sys
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))

from validate_team_map import validate  # noqa: E402


class TestValidateTeamMap(unittest.TestCase):

    def setUp(self) -> None:
        self.valid_data = {
            "board": {
                "id": "1234",
                "project_keys": ["PROJ"],
            },
            "defaults": {
                "dry_run": True,
                "backlog_jql": "project in (PROJ)",
                "active_sprint_jql": "project in (PROJ) AND sprint in openSprints()",
                "stale_after_days": 3,
            },
            "approval": {
                "assignee_change_requires_approval": True,
                "allow_apply_without_approval": False,
                "assigning_authorities": [
                    {
                        "name": "Team Lead",
                        "jira_assignee": "lead@example.com",
                        "scope": ["PROJ"],
                    }
                ],
            },
            "team": [
                {
                    "name": "Team Lead",
                    "jira_assignee": "lead@example.com",
                    "skills": ["backend", "lead"],
                    "max_in_progress": 3,
                    "sprint_capacity_points": 15,
                },
                {
                    "name": "Engineer One",
                    "jira_assignee": "engineer.one@example.com",
                    "skills": ["frontend"],
                    "max_in_progress": 2,
                    "sprint_capacity_points": 8,
                },
            ],
            "rules": {
                "ownership_order": ["component", "label", "skill", "history"],
            },
        }

    def test_valid_team_map_passes(self) -> None:
        errors = validate(self.valid_data)
        self.assertEqual(errors, [])

    def test_missing_board_fails(self) -> None:
        data = dict(self.valid_data)
        del data["board"]
        errors = validate(data)
        self.assertTrue(any("Missing required top-level key: 'board'" in e for e in errors))

    def test_missing_project_keys_fails(self) -> None:
        data = dict(self.valid_data)
        data["board"] = {"id": "1234", "project_keys": []}
        errors = validate(data)
        self.assertTrue(any("project_keys must be a non-empty list" in e for e in errors))

    def test_missing_approval_authorities_fails(self) -> None:
        data = dict(self.valid_data)
        data["approval"] = {"assigning_authorities": []}
        errors = validate(data)
        self.assertTrue(any("assigning_authorities must be a non-empty list" in e for e in errors))

    def test_negative_wip_limit_fails(self) -> None:
        data = dict(self.valid_data)
        data["team"] = [
            {
                "name": "Bad Engineer",
                "jira_assignee": "bad@example.com",
                "skills": ["frontend"],
                "max_in_progress": -1,
                "sprint_capacity_points": 8,
            }
        ]
        errors = validate(data)
        self.assertTrue(any("max_in_progress must be a positive integer" in e for e in errors))

    def test_duplicate_jira_assignee_fails(self) -> None:
        data = dict(self.valid_data)
        data["team"] = [
            {
                "name": "Eng 1",
                "jira_assignee": "dup@example.com",
                "skills": ["frontend"],
                "max_in_progress": 2,
                "sprint_capacity_points": 8,
            },
            {
                "name": "Eng 2",
                "jira_assignee": "dup@example.com",
                "skills": ["backend"],
                "max_in_progress": 2,
                "sprint_capacity_points": 8,
            },
        ]
        errors = validate(data)
        self.assertTrue(any("appears more than once" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
