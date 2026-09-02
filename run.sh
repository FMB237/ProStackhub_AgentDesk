#!/usr/bin/env bash
set -e

# Run AgentDesk with Uvicorn
# Usage: ./run.sh

# Load environment variables if .env exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
