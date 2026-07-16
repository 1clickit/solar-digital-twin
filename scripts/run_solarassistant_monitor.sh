#!/usr/bin/env bash

set -euo pipefail

SERVICE_USER=solardt-sa
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)
MODULE=solar_digital_twin.reporting.solarassistant_monitor

usage() {
    echo "Usage: $0 [--check] [--evidence-dir PATH] [--raw-file PATH] [--bind ADDRESS] [--port PORT] [--capture-duration SECONDS] [--freshness-seconds SECONDS]"
}

python_command() {
    if [[ -x $REPO_ROOT/.venv/bin/python ]]; then
        PYTHON_BIN=$REPO_ROOT/.venv/bin/python
        PYTHON_ENV=()
    else
        PYTHON_BIN=python3
        PYTHON_ENV=(env PYTHONPATH="$REPO_ROOT/src")
    fi
}

check_source() {
    python_command
    command -v "$PYTHON_BIN" >/dev/null
    "${PYTHON_ENV[@]}" "$PYTHON_BIN" -m "$MODULE" --help >/dev/null
    for path in \
        src/solar_digital_twin/reporting/solarassistant_monitor.py \
        scripts/run_solarassistant_monitor.sh; do
        git -C "$REPO_ROOT" ls-files --error-unmatch "$path" >/dev/null 2>&1 || \
            [[ -f $REPO_ROOT/$path ]]
    done
    echo "CHECK: SolarAssistant monitor module and launcher inputs passed"
    echo "CHECK: no root, credential, evidence, collector, device, service, or network action occurred"
}

if [[ ${1-} == --check ]]; then
    [[ $# -eq 1 ]] || { usage >&2; exit 2; }
    check_source
    exit 0
fi

for argument in "$@"; do
    if [[ ${argument,,} == *password* || ${argument,,} == *credential* || ${argument,,} == *secret* ]]; then
        echo "ERROR: credential-like monitor arguments are not accepted" >&2
        exit 2
    fi
done

if [[ $(id -un) != "$SERVICE_USER" ]]; then
    echo "ERROR: real monitor operation must run as $SERVICE_USER" >&2
    exit 1
fi

python_command
bind=127.0.0.1
port=8792
args=("$@")
for ((index=0; index < ${#args[@]}; index++)); do
    case ${args[index]} in
        --bind) index=$((index + 1)); bind=${args[index]-} ;;
        --port) index=$((index + 1)); port=${args[index]-} ;;
        --evidence-dir|--raw-file|--capture-duration|--freshness-seconds) index=$((index + 1)); [[ -n ${args[index]-} ]] || { usage >&2; exit 2; } ;;
        *) usage >&2; exit 2 ;;
    esac
done

echo "SolarAssistant monitor browser URL: http://$bind:$port"
echo "Running in foreground; Ctrl+C stops only the monitor."
exec "${PYTHON_ENV[@]}" "$PYTHON_BIN" -m "$MODULE" "$@"
