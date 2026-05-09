#!/usr/bin/env bash
# Hot-reload Prometheus config without restarting the container.
# Requires --web.enable-lifecycle flag (already set in docker-compose.yml).
#
# Usage: bash scripts/reload-prometheus.sh
set -euo pipefail

PROM_URL="${PROM_URL:-http://localhost:9090}"

echo "==> Validating config first ..."
bash "$(dirname "$0")/validate-config.sh"

echo
echo "==> Reloading $PROM_URL ..."
curl -sf -X POST "$PROM_URL/-/reload" && echo "OK - reload accepted."
