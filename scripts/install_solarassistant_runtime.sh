#!/usr/bin/env bash

set -euo pipefail

SERVICE_USER=solardt-sa
SERVICE_GROUP=solardt-sa
RUNTIME_ROOT=/opt/solar-digital-twin
CREDENTIAL_ROOT=/etc/solar-digital-twin/solarassistant
STATE_ROOT=/var/lib/solar-digital-twin/solarassistant
EVIDENCE_ROOT=$STATE_ROOT/evidence
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)

usage() {
    echo "Usage: $0 [--check|--verify]"
}

check_source() {
    echo "Checking SolarAssistant runtime installation inputs"
    command -v git >/dev/null
    command -v python3 >/dev/null
    command -v tar >/dev/null
    git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null
    for path in \
        requirements.txt \
        pyproject.toml \
        src/solar_digital_twin/collectors/solarassistant.py; do
        git -C "$REPO_ROOT" ls-files --error-unmatch "$path" >/dev/null
    done
    if git -C "$REPO_ROOT" status --porcelain | grep -q .; then
        echo "CHECK: working tree has changes; real installation would refuse"
    else
        echo "CHECK: working tree is clean"
    fi
    if git -C "$REPO_ROOT" ls-files | grep -Eq '(^|/)(password|.*\.env)$'; then
        echo "ERROR: a credential-like file is tracked" >&2
        return 1
    fi
    echo "CHECK: deployment source is tracked Git content only"
    echo "CHECK: no users, paths, packages, credentials, services, or network were changed"
}

require_root() {
    if [[ $EUID -ne 0 ]]; then
        echo "ERROR: administrator privilege is required" >&2
        exit 1
    fi
}

verify_metadata() {
    require_root
    getent passwd "$SERVICE_USER" >/dev/null
    getent group "$SERVICE_GROUP" >/dev/null
    [[ $(id -u "$SERVICE_USER") -lt 1000 ]]
    [[ $(id -Gn "$SERVICE_USER") == "$SERVICE_GROUP" ]]
    [[ $(getent passwd "$SERVICE_USER" | cut -d: -f6) == /nonexistent ]]
    [[ $(getent passwd "$SERVICE_USER" | cut -d: -f7) == /usr/sbin/nologin ]]
    [[ $(stat -c '%U:%G:%a' "$CREDENTIAL_ROOT") == "root:$SERVICE_GROUP:750" ]]
    [[ $(stat -c '%U:%G:%a' "$STATE_ROOT") == "$SERVICE_USER:$SERVICE_GROUP:750" ]]
    [[ $(stat -c '%U:%G:%a' "$EVIDENCE_ROOT") == "$SERVICE_USER:$SERVICE_GROUP:750" ]]
    [[ ! -L $RUNTIME_ROOT && -d $RUNTIME_ROOT ]]
    [[ ! -L $CREDENTIAL_ROOT/password ]]
    if [[ -e $CREDENTIAL_ROOT/password ]]; then
        [[ -f $CREDENTIAL_ROOT/password ]]
        [[ $(stat -c '%U:%G:%a' "$CREDENTIAL_ROOT/password") == "root:$SERVICE_GROUP:640" ]]
        runuser -u "$SERVICE_USER" -- test -r "$CREDENTIAL_ROOT/password"
        ! runuser -u "$SERVICE_USER" -- test -w "$CREDENTIAL_ROOT/password"
        ! runuser -u "$SERVICE_USER" -- test -w "$CREDENTIAL_ROOT"
    fi
    ! runuser -u "$SERVICE_USER" -- test -w "$RUNTIME_ROOT"
    probe=$EVIDENCE_ROOT/.runtime-write-check.$$
    runuser -u "$SERVICE_USER" -- touch "$probe"
    rm -f -- "$probe"
    runuser -u "$SERVICE_USER" -- \
        "$RUNTIME_ROOT/.venv/bin/python" -m \
        solar_digital_twin.collectors.solarassistant --help >/dev/null
    echo "VERIFY: SolarAssistant runtime metadata and access boundaries passed"
}

install_runtime() {
    require_root
    if [[ $# -ne 0 ]]; then
        usage >&2
        exit 2
    fi
    if [[ -n $(git -C "$REPO_ROOT" status --porcelain) ]]; then
        echo "ERROR: installation requires a clean working tree" >&2
        exit 1
    fi

    getent group "$SERVICE_GROUP" >/dev/null || \
        groupadd --system "$SERVICE_GROUP"
    if getent passwd "$SERVICE_USER" >/dev/null; then
        [[ $(id -u "$SERVICE_USER") -lt 1000 ]]
        [[ $(id -gn "$SERVICE_USER") == "$SERVICE_GROUP" ]]
        [[ $(id -Gn "$SERVICE_USER") == "$SERVICE_GROUP" ]]
        [[ $(getent passwd "$SERVICE_USER" | cut -d: -f6) == /nonexistent ]]
        [[ $(getent passwd "$SERVICE_USER" | cut -d: -f7) == /usr/sbin/nologin ]]
    else
        useradd --system --gid "$SERVICE_GROUP" --no-create-home \
            --home-dir /nonexistent --shell /usr/sbin/nologin "$SERVICE_USER"
    fi

    install -d -o root -g root -m 0755 /etc/solar-digital-twin
    install -d -o root -g "$SERVICE_GROUP" -m 0750 "$CREDENTIAL_ROOT"
    install -d -o "$SERVICE_USER" -g "$SERVICE_GROUP" -m 0750 \
        "$STATE_ROOT" "$EVIDENCE_ROOT"

    stage=/opt/.solar-digital-twin.new.$$
    backup=
    cleanup() { rm -rf -- "$stage"; }
    trap cleanup EXIT
    install -d -o root -g root -m 0755 "$stage"
    git -C "$REPO_ROOT" archive --format=tar HEAD | tar -x -C "$stage"
    chown -R root:root "$stage"
    chmod -R u=rwX,go=rX "$stage"

    if [[ -e $RUNTIME_ROOT ]]; then
        backup=/opt/solar-digital-twin.backup.$(date -u +%Y%m%dT%H%M%SZ)
        mv -- "$RUNTIME_ROOT" "$backup"
    fi
    mv -- "$stage" "$RUNTIME_ROOT"
    trap - EXIT

    install_complete=0
    report_partial_failure() {
        if [[ $install_complete -eq 0 ]]; then
            echo "ERROR: runtime preparation stopped after deployment; review $RUNTIME_ROOT before use" >&2
            [[ -z $backup ]] || echo "Previous runtime remains at $backup" >&2
        fi
    }
    trap report_partial_failure EXIT

    python3 -m venv "$RUNTIME_ROOT/.venv"
    "$RUNTIME_ROOT/.venv/bin/pip" install \
        --requirement "$RUNTIME_ROOT/requirements.txt"
    "$RUNTIME_ROOT/.venv/bin/pip" install "$RUNTIME_ROOT"
    chown -R root:root "$RUNTIME_ROOT"
    chmod -R u=rwX,go=rX "$RUNTIME_ROOT"
    install_complete=1
    trap - EXIT

    echo "Installed SolarAssistant runtime without a credential or service"
    [[ -z $backup ]] || echo "Previous runtime preserved at $backup"
    echo "Credential installation and manual verification require separate approval"
}

case ${1-} in
    --check)
        [[ $# -eq 1 ]] || { usage >&2; exit 2; }
        check_source
        ;;
    --verify)
        [[ $# -eq 1 ]] || { usage >&2; exit 2; }
        verify_metadata
        ;;
    "")
        install_runtime
        ;;
    *)
        usage >&2
        exit 2
        ;;
esac
