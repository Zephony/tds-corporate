#!/bin/bash

# Stop app and cleanup port assignment
# Usage: ./scripts/stop-app.sh

set -e

echo '🛑 Stopping application...'

# Check if docker compose is available
if docker compose version >/dev/null 2>&1; then
  COMPOSE='docker compose'
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE='docker-compose'
else
  echo '❌ Docker Compose is required'
  exit 1
fi

# Stop the application
$COMPOSE -f docker-compose.yml -f docker-compose.production.yml down

# Cleanup port assignment
if [ -f "scripts/cleanup-ports.sh" ]; then
  ./scripts/cleanup-ports.sh
else
  echo '⚠️  Port cleanup script not found, port may not be released'
fi

echo '✅ Application stopped and port released'
