PYTHON ?= python3

.PHONY: help test validate check-env setup install clean verify-mcp cron-install docker-build docker-up docker-down

help:
	@echo "Sprint Guardian — Available Commands:"
	@echo "  make setup         Run the interactive setup wizard"
	@echo "  make test          Run the complete automated test suite"
	@echo "  make validate      Validate team-map and skill configuration"
	@echo "  make check-env     Check runtime environment readiness"
	@echo "  make verify-mcp    Verify Jira API & MCP server credentials"
	@echo "  make install       Install / link skill to ~/.codex/skills/ & ~/.claude/skills/"
	@echo "  make cron-install  Install automated cron schedules to system crontab"
	@echo "  make docker-build  Build Docker deployment image"
	@echo "  make docker-up     Start scheduled container daemon via docker compose"
	@echo "  make docker-down   Stop scheduled container daemon"
	@echo "  make clean         Remove temporary files and logs"

setup:
	@./automation/setup.sh

test:
	@$(PYTHON) tests/run_tests.py

validate:
	@./automation/validate-skill.sh

check-env:
	@$(PYTHON) scripts/check_env.py

verify-mcp:
	@$(PYTHON) scripts/verify_mcp_connection.py

install:
	@./automation/install-skill.sh

cron-install:
	@./scripts/install_cron.sh

docker-build:
	@docker build -t sprint-guardian .

docker-up:
	@docker compose up -d sprint-guardian

docker-down:
	@docker compose down

clean:
	@rm -rf automation/output/*.md automation/output/*.log
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleaned temporary files and test output."
