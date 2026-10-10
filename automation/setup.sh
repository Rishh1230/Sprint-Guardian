#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_CMD="python3"

for candidate in \
  "${ROOT_DIR}/.venv-jira-tools/bin/python" \
  "${ROOT_DIR}/../.venv-jira-tools/bin/python" \
  "${VIRTUAL_ENV:-}/bin/python" \
  "python3" \
  "python"; do
  if [[ -n "$candidate" ]] && command -v "$candidate" >/dev/null 2>&1; then
    PYTHON_CMD="$candidate"
    break
  fi
done

exec "$PYTHON_CMD" "$ROOT_DIR/scripts/setup_wizard.py" "$@"
