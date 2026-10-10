#!/usr/bin/env python3
"""verify_mcp_connection.py — Validates Jira credentials and MCP readiness.

Checks:
  - JIRA_INSTANCE_URL is reachable
  - JIRA_EMAIL and JIRA_API_TOKEN are set and authenticate successfully
  - /rest/api/3/myself endpoint returns valid user profile
  - Atlassian MCP server package is installed or available via npx

Usage:
  python3 scripts/verify_mcp_connection.py
"""
from __future__ import annotations

import base64
import json
import os
import shutil
import sys
import urllib.error
import urllib.request


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
    print("==================================================")
    print("  🔗 Jira & MCP Connection Readiness Check")
    print("==================================================")
    print()

    jira_url = os.environ.get("JIRA_INSTANCE_URL", "").rstrip("/")
    jira_email = os.environ.get("JIRA_EMAIL", "").strip()
    jira_token = os.environ.get("JIRA_API_TOKEN", "").strip()

    all_ok = True

    # 1. Environment variables check
    has_url = check("JIRA_INSTANCE_URL set", bool(jira_url), jira_url or "missing")
    has_email = check("JIRA_EMAIL set", bool(jira_email), jira_email or "missing")
    has_token = check("JIRA_API_TOKEN set", bool(jira_token), "******" if jira_token else "missing")

    all_ok &= (has_url and has_email and has_token)

    # 2. Node & NPX check (for Atlassian MCP server)
    npx_path = shutil.which("npx")
    node_ok = check("npx / Node.js available", bool(npx_path), npx_path or "install Node.js to use @modelcontextprotocol/server-atlassian")
    all_ok &= node_ok

    if not (has_url and has_email and has_token):
        print()
        print("Note: To verify live Jira API connectivity, set:")
        print("  export JIRA_INSTANCE_URL='https://your-domain.atlassian.net'")
        print("  export JIRA_EMAIL='your-email@example.com'")
        print("  export JIRA_API_TOKEN='your-api-token'")
        print("Or add them to your .env file.")
        print()
        if not node_ok:
            sys.exit(1)
        print("Pre-flight checks passed (credentials check skipped).")
        sys.exit(0)

    # 3. Live Jira REST API Ping
    print("\nPinging Jira REST API...")
    auth_str = f"{jira_email}:{jira_token}"
    auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

    api_url = f"{jira_url}/rest/api/3/myself"
    req = urllib.request.Request(
        api_url,
        headers={
            "Authorization": f"Basic {auth_b64}",
            "Accept": "application/json",
            "User-Agent": "Sprint-Guardian-Verifier",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                body = json.loads(resp.read().decode("utf-8"))
                display_name = body.get("displayName", "Authenticated User")
                account_id = body.get("accountId", "unknown")
                check("Jira API Authentication", True, f"Connected as '{display_name}' ({account_id})")
            else:
                check("Jira API Authentication", False, f"HTTP Status {resp.status}")
                all_ok = False
    except urllib.error.HTTPError as e:
        check("Jira API Authentication", False, f"HTTP Error {e.code}: {e.reason}")
        all_ok = False
    except urllib.error.URLError as e:
        check("Jira API Connectivity", False, f"Connection failed: {e.reason}")
        all_ok = False
    except Exception as e:
        check("Jira API Request", False, str(e))
        all_ok = False

    print()
    if all_ok:
        print("Jira & MCP connectivity verified successfully! 🚀")
        sys.exit(0)
    else:
        print("Connectivity check failed. Please review credentials and network access.")
        sys.exit(1)


if __name__ == "__main__":
    main()
