#!/usr/bin/env bash
# List every scrape target with its health and last error (if any).
# Requires: jq, curl, running Prometheus on localhost:9090.
#
# Usage: bash scripts/check-targets.sh
set -euo pipefail

PROM_URL="${PROM_URL:-http://localhost:9090}"

curl -sf "$PROM_URL/api/v1/targets" \
  | jq -r '.data.activeTargets[]
      | "\(.labels.job)\t\(.scrapeUrl)\t\(.health)\t\(.lastError // "-")"' \
  | column -t -s $'\t'
