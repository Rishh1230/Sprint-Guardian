#!/usr/bin/env python3
"""test_shell_scripts.py — Verifies bash script syntax and executable permissions."""
from __future__ import annotations

import glob
import os
import subprocess
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTOMATION_DIR = os.path.join(ROOT_DIR, "automation")


class TestShellScripts(unittest.TestCase):

    def test_scripts_syntax(self) -> None:
        scripts = glob.glob(os.path.join(AUTOMATION_DIR, "*.sh"))
        self.assertGreater(len(scripts), 0, "No shell scripts found in automation/")

        for script in scripts:
            res = subprocess.run(
                ["bash", "-n", script],
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                res.returncode,
                0,
                f"Syntax error in {os.path.basename(script)}:\n{res.stderr}",
            )

    def test_scripts_executable_permission(self) -> None:
        scripts = glob.glob(os.path.join(AUTOMATION_DIR, "*.sh"))
        for script in scripts:
            is_executable = os.access(script, os.X_OK)
            self.assertTrue(
                is_executable,
                f"Script {os.path.basename(script)} is missing executable (+x) permissions",
            )


if __name__ == "__main__":
    unittest.main()
