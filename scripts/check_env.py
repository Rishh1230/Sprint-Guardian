#!/usr/bin/env python3
"""check_env.py — Checks that the Sprint Guardian runtime environment is ready.

Verifies:
  - Python version >= 3.8
  - pyyaml is importable
  - codex CLI is on PATH
  - team-map.local.yaml exists (optional warning if not)
  - .env file exists (optional warning if not)

Usage:
    python scripts/check_env.py
"""
from __future__ import annotations

import os
import shutil
import sys


def check(label: str, ok: bool, detail: str = "") -> bool:
    status = "✅" if ok else "❌"
    msg = f"  {status}  {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return ok


def warn(label: str, detail: str = "") -> None:
    msg = f"  ⚠️   {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)


def main() -> None:
    print()
    print("Sprint Guardian — Environment Check")
    print("=" * 50)
    print()

    all_ok = True

    # Python version
    py_ok = sys.version_info >= (3, 8)
    v = sys.version_info
    all_ok &= check(
        "Python >= 3.8",
        py_ok,
        f"{v.major}.{v.minor}.{v.micro}" + ("" if py_ok else " — please upgrade to 3.8+"),
    )

    # PyYAML
    try:
        import yaml  # noqa: F401
        yaml_ok = True
        yaml_detail = ""
    except ImportError:
        yaml_ok = False
        yaml_detail = "run: pip install pyyaml"
    all_ok &= check("pyyaml importable", yaml_ok, yaml_detail)

    # codex CLI
    codex_path = shutil.which("codex")
    codex_ok = codex_path is not None
    all_ok &= check(
        "codex CLI on PATH",
        codex_ok,
        codex_path or "not found — install Codex CLI from https://github.com/openai/codex",
    )

    # team map
    team_map = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "references",
        "team-map.local.yaml",
    )
    if os.path.isfile(team_map):
        check("references/team-map.local.yaml exists", True)
    else:
        warn(
            "references/team-map.local.yaml not found",
            "copy from team-map.example.yaml and fill in your team details",
        )

    # .env file
    env_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".env",
    )
    if os.path.isfile(env_file):
        check(".env file exists", True)
    else:
        warn(
            ".env file not found",
            "copy from .env.example — environment variables are optional but convenient",
        )

    print()
    if all_ok:
        print("All required checks passed. Sprint Guardian is ready to run. 🚀")
    else:
        print("One or more required checks failed. Fix the issues above and re-run.")
        sys.exit(1)
    print()


if __name__ == "__main__":
    main()
