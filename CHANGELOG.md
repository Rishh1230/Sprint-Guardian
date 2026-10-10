# Changelog

All notable changes to `sprint-guardian` will be documented here.

Format: [Semantic Versioning](https://semver.org/). Types: `Added`, `Changed`, `Fixed`, `Removed`.

## [1.2.0] - 2026-10-10

### Added
- `scripts/setup_wizard.py` & `automation/setup.sh`: Interactive terminal onboarding wizard that configures `references/team-map.local.yaml` and `.env` in under 2 minutes.
- `tests/run_tests.py`: Unified test runner discovering and executing all automated tests.
- `tests/test_validate_team_map.py`: Unit test suite for team map schema validation, WIP limit rules, and duplicate assignee detection.
- `tests/test_prompts.py`: Automated checks ensuring all 9 operational prompt templates exist and enforce approval guardrails on mutation modes.
- `tests/test_shell_scripts.py`: Syntax verification (`bash -n`) and executable permission audits for all shell scripts.
- `tests/fixtures/mock_jira_issues.json`: Realistic Jira mock payload fixture for offline testing.
- `Makefile`: Common developer shortcuts (`make setup`, `make test`, `make validate`, `make check-env`, `make install`, `make clean`).
- `.github/workflows/ci.yml`: GitHub Actions matrix CI workflow testing against Python 3.9 through 3.13.
- `agents/claude-desktop-mcp.example.json`: Configuration snippet for connecting Atlassian MCP to Claude Desktop.

---

## [1.1.0] - 2026-10-10

### Fixed
- `validate-skill.sh`: Replaced hardcoded `/Users/ghansgup/...` validator path with `${CODEX_HOME:-$HOME/.codex}/...` so the script works on any machine.
- `run-sprint-guardian.sh`: `codex exec` failures now log `status=failed` to the approval audit log instead of `status=completed`.
- `run-sprint-guardian.sh`: Missing venv Python during `validate_approval_authority` is now a hard `exit 1` instead of `return 1`, preventing silent approval bypass.
- `run-sprint-guardian.sh`: Narrowed `ASSIGNEE_CHANGE_CAPABLE` to only `suggest-owner` and `balance-load` (was incorrectly including `inspect-sprint` and `surface-risk`).
- `cron.example`: Replaced hardcoded Linux `/home/developer/...` paths with `YOUR/WORKSPACE/PATH` placeholder comments.
- `README.md`: Corrected Codex CLI prerequisite from "optional" to "required".
- `references/jira-query-guide.md`: Added note to keep the `-3d` stale threshold in sync with `stale_after_days` in team map.
- `references/team-map.example.yaml`: Clarified that the `audit_log` field is informational only; actual path is always set by the orchestrator.

### Added
- `automation/output/.gitignore`: Prevents accidental commits of generated sprint output and approval log files.
- `run-sprint-guardian.sh`: `--debug` flag enables `set -x` for shell trace debugging.
- `run-sprint-guardian.sh`: Run-mode banner printed at startup showing mode, dry-run/apply status, and approval authority.
- `run-sprint-guardian.sh`: Conflict warning when both `--project-key` and `--project-keys` are supplied.
- `agents/openai.yaml`: Added `interface.version: "1"` field.
- `CHANGELOG.md`: This file.

### Removed
- All `automation/prompts/*.md` files: Removed redundant attribution headers (present in `SKILL.md`, wasteful in prompts consumed by the orchestrator).

---

## [1.0.0] - Initial Release

- Initial release of Sprint Guardian skill.
