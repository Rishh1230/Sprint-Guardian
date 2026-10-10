#!/usr/bin/env bash
# docker-entrypoint.sh — Docker container entrypoint for Sprint Guardian.

set -euo pipefail

cd /app

# Run environment checks
if [[ "${SKIP_ENV_CHECK:-false}" != "true" ]]; then
  echo "Running pre-flight checks..."
  python3 scripts/check_env.py || true
fi

# Mode 1: Start background cron daemon
if [[ "${1:-}" == "cron-daemon" ]]; then
  echo "Starting Sprint Guardian in scheduled Cron Daemon mode..."
  ./scripts/install_cron.sh
  # Run cron in foreground to keep container alive
  exec cron -f
fi

# Mode 2: Run test suite
if [[ "${1:-}" == "test" ]]; then
  exec python3 tests/run_tests.py
fi

# Mode 3: Run interactive setup
if [[ "${1:-}" == "setup" ]]; then
  exec ./automation/setup.sh
fi

# Mode 4: Run a specific sprint guardian mode (e.g. shape-sprint, standup-brief, etc.)
if [[ -f "/app/automation/${1:-}.sh" ]]; then
  MODE_SCRIPT="/app/automation/${1}.sh"
  shift
  exec "$MODE_SCRIPT" "$@"
fi

# Mode 5: Pass-through command
exec "$@"
