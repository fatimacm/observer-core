#!/bin/bash
# smoke-test.sh – Minimal smoke test for observer-core
# Exits with 0 if all endpoints are healthy, non-zero otherwise.
set -e

BASE_URL="${BASE_URL:-http://localhost:8000}"  # Configurable via env var
ENDPOINTS=("/health" "/status" "/metrics")

echo "[Smoke Test] Checking observer-core at $BASE_URL"

for endpoint in "${ENDPOINTS[@]}"; do
  echo -n "Testing $endpoint ... "
  if curl -fs -o /dev/null "$BASE_URL$endpoint"; then
    echo "OK"
  else
    echo "FAIL"
    exit 1
  fi
done

echo "[Smoke Test] All endpoints reachable ✅"
exit 0