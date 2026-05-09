#!/usr/bin/env bash
# Validate prometheus.yml and rule files using promtool inside the Prometheus
# container. Run from the lab root directory.
#
# Usage: bash scripts/validate-config.sh
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> Checking prometheus.yml ..."
docker run --rm \
  -v "$PWD/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro" \
  -v "$PWD/prometheus/rules:/etc/prometheus/rules:ro" \
  prom/prometheus:v2.55.1 \
  promtool check config /etc/prometheus/prometheus.yml

echo
echo "==> Checking alert rules ..."
docker run --rm \
  -v "$PWD/prometheus/rules:/etc/prometheus/rules:ro" \
  prom/prometheus:v2.55.1 \
  promtool check rules /etc/prometheus/rules/alerts.yml

echo
echo "OK - configs valid."
