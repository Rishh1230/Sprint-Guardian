#!/usr/bin/env python3
"""run_tests.py — Runs the complete test suite for Sprint Guardian."""
from __future__ import annotations

import os
import sys
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(ROOT_DIR, "tests")

# Add scripts directory to path
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))


def main() -> None:
    print("==================================================")
    print("  🧪 Sprint Guardian — Test Suite")
    print("==================================================")
    print()

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=TESTS_DIR, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    if result.wasSuccessful():
        print("✅ All tests passed successfully!")
        sys.exit(0)
    else:
        print(f"❌ Test run failed: {len(result.failures)} failures, {len(result.errors)} errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()
