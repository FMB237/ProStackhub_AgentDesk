#!/usr/bin/env bash
set -e

URL="${1:-http://localhost:8000/health}"

echo "Checking health endpoint: $URL"
if curl -sSf "$URL" > /tmp/health.json; then
  echo "✅ Service is healthy"
  cat /tmp/health.json | python3 -m json.tool
  exit 0
else
  echo "❌ Health check failed"
  exit 1
fi
