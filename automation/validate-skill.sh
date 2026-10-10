#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_CMD=""

for candidate in \
  "${ROOT_DIR}/.venv-jira-tools/bin/python" \
  "${ROOT_DIR}/../.venv-jira-tools/bin/python" \
  "${VIRTUAL_ENV:-}/bin/python" \
  "python3" \
  "python"; do
  if [[ -n "$candidate" ]] && command -v "$candidate" >/dev/null 2>&1; then
    if "$candidate" -c "import yaml" >/dev/null 2>&1; then
      PYTHON_CMD="$candidate"
      break
    elif [[ -z "$PYTHON_CMD" ]]; then
      PYTHON_CMD="$candidate"
    fi
  fi
done

if [[ -z "$PYTHON_CMD" ]]; then
  printf 'Python 3 is required but not found on PATH.\n' >&2
  exit 1
fi

printf '=== Sprint Guardian Validator ===\n\n'

# 1. Validate team map if present (or example map as baseline)
TEAM_MAP_TO_CHECK="$ROOT_DIR/references/team-map.local.yaml"
if [[ ! -f "$TEAM_MAP_TO_CHECK" ]]; then
  TEAM_MAP_TO_CHECK="$ROOT_DIR/references/team-map.example.yaml"
  printf 'Notice: team-map.local.yaml not found. Validating team-map.example.yaml instead...\n\n'
fi

"$PYTHON_CMD" "$ROOT_DIR/scripts/validate_team_map.py" "$TEAM_MAP_TO_CHECK"
printf '\n'

# 2. Check SKILL.md structure
if [[ ! -f "$ROOT_DIR/SKILL.md" ]]; then
  printf '[ERROR] SKILL.md missing at root directory!\n' >&2
  exit 1
fi
printf '[OK]    SKILL.md found and readable.\n'

# 3. Optional quick_validate from skill-creator if installed in Codex environment
VALIDATOR="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py"
TARGET="${1:-$ROOT_DIR}"

if [[ -f "$VALIDATOR" ]]; then
  printf '\nRunning Codex skill-creator validator...\n'
  "$PYTHON_CMD" "$VALIDATOR" "$TARGET"
else
  printf '[INFO]  Codex skill-creator validator not installed at %s (skipped).\n' "$VALIDATOR"
fi

printf '\n=== Validation Complete ===\n'

