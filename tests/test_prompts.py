#!/usr/bin/env python3
"""test_prompts.py — Validates that all 9 operational prompt files exist and conform to standards."""
from __future__ import annotations

import os
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS_DIR = os.path.join(ROOT_DIR, "automation", "prompts")

EXPECTED_MODES = [
    "shape-sprint",
    "triage-queue",
    "suggest-owner",
    "balance-load",
    "inspect-sprint",
    "surface-risk",
    "progress-pulse",
    "standup-brief",
    "retro-notes",
]


class TestPrompts(unittest.TestCase):

    def test_all_prompts_exist(self) -> None:
        for mode in EXPECTED_MODES:
            path = os.path.join(PROMPTS_DIR, f"{mode}.md")
            self.assertTrue(
                os.path.isfile(path),
                f"Missing prompt file for mode: {mode} at {path}",
            )

    def test_prompts_have_required_sections(self) -> None:
        for mode in EXPECTED_MODES:
            path = os.path.join(PROMPTS_DIR, f"{mode}.md")
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()

            self.assertIn("Goal:", content, f"Prompt {mode}.md missing 'Goal:'")
            self.assertIn(
                "Required Behavior",
                content,
                f"Prompt {mode}.md missing 'Required Behavior' section",
            )
            self.assertIn(
                "Output Requirements",
                content,
                f"Prompt {mode}.md missing 'Output Requirements' section",
            )

    def test_prompts_enforce_approval_rules(self) -> None:
        # Mutation-capable modes must explicitly mention approval / approved-by
        mutation_modes = ["shape-sprint", "triage-queue", "suggest-owner", "balance-load"]
        for mode in mutation_modes:
            path = os.path.join(PROMPTS_DIR, f"{mode}.md")
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read().lower()

            self.assertTrue(
                "approval" in content or "approved-by" in content,
                f"Mutation mode {mode}.md must mention approval rules",
            )


if __name__ == "__main__":
    unittest.main()
