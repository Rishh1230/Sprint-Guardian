#!/usr/bin/env bash
# install_cron.sh — Installs automated Sprint Guardian cron jobs into crontab.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="${ROOT_DIR}/automation/output/cron-logs"

mkdir -p "$LOG_DIR"

BOARD_ID="${SPRINT_ASSIGNER_BOARD_ID:-1234}"
PROJECT_KEY="${SPRINT_ASSIGNER_PROJECT_KEYS:-PROJ}"

echo "=================================================="
echo "  Installing Sprint Guardian Cron Jobs"
echo "=================================================="
echo "Workspace:   $ROOT_DIR"
echo "Log dir:     $LOG_DIR"
echo "Board ID:    $BOARD_ID"
echo "Project Key: $PROJECT_KEY"
echo

CRON_TAG="# SPRINT_GUARDIAN_CRON"

# Build new cron entries
NEW_ENTRIES=$(cat <<EOF
$CRON_TAG - BEGIN
# Monday 9:00 AM — Shape next sprint scope
0 9 * * 1 cd "$ROOT_DIR" && ./automation/shape-sprint.sh --board-id "$BOARD_ID" --project-key "$PROJECT_KEY" >> "$LOG_DIR/shape-sprint.log" 2>&1
# Weekdays 9:30 AM — Daily standup brief
30 9 * * 1-5 cd "$ROOT_DIR" && ./automation/standup-brief.sh --board-id "$BOARD_ID" --project-key "$PROJECT_KEY" >> "$LOG_DIR/standup-brief.log" 2>&1
# Weekdays 1:00 PM — Daily progress pulse
0 13 * * 1-5 cd "$ROOT_DIR" && ./automation/progress-pulse.sh --board-id "$BOARD_ID" >> "$LOG_DIR/progress-pulse.log" 2>&1
# Tuesday & Thursday 4:00 PM — Surface delivery risks
0 16 * * 2,4 cd "$ROOT_DIR" && ./automation/surface-risk.sh --board-id "$BOARD_ID" >> "$LOG_DIR/surface-risk.log" 2>&1
$CRON_TAG - END
EOF
)

# Read existing crontab without previous Sprint Guardian entries
EXISTING_CRONTAB=""
if crontab -l 2>/dev/null; then
  EXISTING_CRONTAB=$(crontab -l | sed "/$CRON_TAG - BEGIN/,/$CRON_TAG - END/d")
fi

# Combine and install
TMP_CRON="$(mktemp)"
{
  if [[ -n "$EXISTING_CRONTAB" ]]; then
    printf '%s\n' "$EXISTING_CRONTAB"
  fi
  printf '\n%s\n' "$NEW_ENTRIES"
} > "$TMP_CRON"

crontab "$TMP_CRON"
rm -f "$TMP_CRON"

echo "Cron jobs installed successfully."
echo
echo "Installed schedules:"
crontab -l | grep -A 8 "$CRON_TAG - BEGIN"
echo
echo "To view cron logs: tail -f $LOG_DIR/*.log"
echo "To uninstall:      crontab -e and remove the block between $CRON_TAG tags."
echo
