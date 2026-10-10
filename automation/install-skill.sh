#!/usr/bin/env bash
# install-skill.sh — Links skill into Codex and/or Claude agent skill directories.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

link_skill() {
  local target_root="$1"
  local agent_name="$2"
  local target_link="$target_root/sprint-guardian"

  mkdir -p "$target_root"

  if [[ -d "$target_link" && ! -L "$target_link" ]]; then
    printf 'Warning: Refusing to replace existing non-symlink directory for %s: %s\n' "$agent_name" "$target_link" >&2
    return 0
  fi

  if [[ -L "$target_link" || -f "$target_link" ]]; then
    rm -f "$target_link"
  fi

  ln -s "$ROOT_DIR" "$target_link"
  printf '[OK] Linked for %s: %s -> %s\n' "$agent_name" "$target_link" "$ROOT_DIR"
}

echo "Installing Sprint Guardian skill..."
echo

# 1. Install for Codex
CODEX_TARGET="${CODEX_HOME:-$HOME/.codex}/skills"
link_skill "$CODEX_TARGET" "Codex"

# 2. Install for Claude Code (if ~/.claude exists)
if [[ -d "$HOME/.claude" ]]; then
  CLAUDE_TARGET="$HOME/.claude/skills"
  link_skill "$CLAUDE_TARGET" "Claude Code"
fi

# 3. Custom target passed via argument
if [[ $# -gt 0 && -n "$1" ]]; then
  link_skill "$1" "Custom Location"
fi

echo
echo "Skill installation complete. You can now invoke \$sprint-guardian in your agent."
