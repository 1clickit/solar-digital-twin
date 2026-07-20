#!/usr/bin/env bash

set -euo pipefail

RUNTIME_ROOT=/opt/solar-digital-twin
EVIDENCE_ROOT=/var/lib/solar-digital-twin/esp32/evidence
DURATION_SECONDS=3600
COMMIT_FILE=$RUNTIME_ROOT/.solardt-installed-commit

[[ -f $COMMIT_FILE && ! -L $COMMIT_FILE ]]
collector_version=$(<"$COMMIT_FILE")
[[ $collector_version =~ ^[0-9a-f]{40}$ ]]

exec "$RUNTIME_ROOT/.venv/bin/python" -m \
    solar_digital_twin.collectors.esp32_sse \
    --duration "$DURATION_SECONDS" \
    --retention-mode current \
    --collector-version "$collector_version" \
    --output-dir "$EVIDENCE_ROOT"
