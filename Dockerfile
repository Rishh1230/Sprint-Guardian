FROM python:3.11-slim

LABEL maintainer="Sprint Guardian Team"
LABEL description="Sprint Guardian — AI-powered Agile Sprint Orchestrator"
LABEL version="1.2.0"

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app

WORKDIR $APP_HOME

# Install system dependencies, Node.js (for Atlassian MCP server), cron, and bash
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    git \
    cron \
    ca-certificates \
    gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure all scripts are executable and use LF line endings
RUN chmod +x automation/*.sh scripts/*.py scripts/*.sh tests/*.py tests/run_tests.py \
    && mkdir -p automation/output/cron-logs

# Default entrypoint and command
ENTRYPOINT ["/app/scripts/docker-entrypoint.sh"]
CMD ["inspect-sprint"]
