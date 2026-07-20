#!/usr/bin/env bash

set -euo pipefail

SERVICE_USER=solardt-telemetry
SERVICE_GROUP=solardt-telemetry
RUNTIME_ROOT=/opt/solar-digital-twin
STATE_ROOT=/var/lib/solar-digital-twin/esp32
EVIDENCE_ROOT=$STATE_ROOT/evidence
UNIT_NAME=esp32-forensic-collector.service
UNIT_SOURCE=systemd/$UNIT_NAME
UNIT_DEST=/etc/systemd/system/$UNIT_NAME
EXPECTED_REMOTE=https://github.com/1clickit/solar-digital-twin.git
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)
REQUIRED_TRACKED=(
    requirements.txt
    pyproject.toml
    src/solar_digital_twin/collectors/esp32_sse.py
    src/solar_digital_twin/collectors/esp32_retention.py
    scripts/install_esp32_runtime.sh
    scripts/run_esp32_forensic_collector.sh
    systemd/esp32-forensic-collector.service
)

usage() {
    echo "Usage: $0 --check | --install [--accept-legacy-runtime] [--reporter USER] | --verify [--reporter USER]"
}

check_source() {
    echo "Checking ESP32 runtime installation inputs"
    command -v git >/dev/null
    command -v python3 >/dev/null
    command -v tar >/dev/null
    command -v cmp >/dev/null
    git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null
    commit=$(git -C "$REPO_ROOT" rev-parse HEAD)
    [[ $commit =~ ^[0-9a-f]{40}$ ]]
    echo "CHECK: source commit $commit"
    for path in "${REQUIRED_TRACKED[@]}"; do
        if git -C "$REPO_ROOT" ls-files --error-unmatch "$path" >/dev/null 2>&1; then
            [[ -f $REPO_ROOT/$path && ! -L $REPO_ROOT/$path ]]
        elif [[ -f $REPO_ROOT/$path && ! -L $REPO_ROOT/$path ]]; then
            echo "CHECK: pending file must be committed before installation: $path"
        else
            echo "ERROR: required regular input is missing: $path" >&2
            return 1
        fi
    done
    [[ -x $REPO_ROOT/scripts/install_esp32_runtime.sh ]]
    [[ -x $REPO_ROOT/scripts/run_esp32_forensic_collector.sh ]]
    if [[ -n $(git -C "$REPO_ROOT" status --porcelain) ]]; then
        echo "CHECK: working tree has changes; installation would refuse"
    else
        echo "CHECK: working tree is clean"
    fi
    remote=$(git -C "$REPO_ROOT" remote get-url origin 2>/dev/null || true)
    if [[ $remote == "$EXPECTED_REMOTE" ]]; then
        echo "CHECK: expected origin is configured"
    else
        echo "CHECK: origin differs or is absent; installation would refuse"
    fi
    if grep -Eq '^(EnvironmentFile|LoadCredential)=' "$REPO_ROOT/$UNIT_SOURCE"; then
        echo "ERROR: ESP32 unit must remain credentialless" >&2
        return 1
    fi
    if grep -Eq '^\[Install\]$' "$REPO_ROOT/$UNIT_SOURCE"; then
        echo "ERROR: ESP32 unit must remain dormant without an install target" >&2
        return 1
    fi
    echo "CHECK: identity=$SERVICE_USER group=$SERVICE_GROUP"
    echo "CHECK: runtime=$RUNTIME_ROOT evidence=$EVIDENCE_ROOT"
    echo "CHECK: tracked whole-application deployment; no credential path"
    echo "CHECK: no installation, identity, service, package, network, device, or evidence change occurred"
    echo "CHECK: no device was contacted"
}

require_root() {
    if [[ $EUID -ne 0 ]]; then
        echo "ERROR: administrator privilege is required" >&2
        exit 1
    fi
}

require_clean_approved_source() {
    [[ -z $(git -C "$REPO_ROOT" status --porcelain) ]] || {
        echo "ERROR: installation requires a clean working tree" >&2
        exit 1
    }
    [[ $(git -C "$REPO_ROOT" remote get-url origin) == "$EXPECTED_REMOTE" ]] || {
        echo "ERROR: unexpected origin URL" >&2
        exit 1
    }
    for path in "${REQUIRED_TRACKED[@]}"; do
        git -C "$REPO_ROOT" ls-files --error-unmatch "$path" >/dev/null
        [[ -f $REPO_ROOT/$path && ! -L $REPO_ROOT/$path ]]
    done
}

verify_identity() {
    getent passwd "$SERVICE_USER" >/dev/null
    getent group "$SERVICE_GROUP" >/dev/null
    [[ $(id -u "$SERVICE_USER") -lt 1000 ]]
    [[ $(id -gn "$SERVICE_USER") == "$SERVICE_GROUP" ]]
    [[ $(id -Gn "$SERVICE_USER") == "$SERVICE_GROUP" ]]
    [[ $(getent passwd "$SERVICE_USER" | cut -d: -f6) == /nonexistent ]]
    [[ $(getent passwd "$SERVICE_USER" | cut -d: -f7) == /usr/sbin/nologin ]]
}

verify_regular_metadata() {
    local path=$1 expected=$2
    [[ ! -L $path && -e $path ]]
    [[ $(stat -c '%U:%G:%a' "$path") == "$expected" ]]
}

create_or_verify_directory() {
    local path=$1 owner=$2 group=$3 mode=$4
    if [[ -e $path ]]; then
        verify_regular_metadata "$path" "$owner:$group:$mode"
        [[ -d $path ]]
    else
        install -d -o "$owner" -g "$group" -m "$mode" "$path"
    fi
}

verify_metadata() {
    local reporter=${1-}
    require_root
    verify_identity
    verify_regular_metadata "$RUNTIME_ROOT" root:root:755
    verify_regular_metadata "$RUNTIME_ROOT/.solardt-installed-commit" root:root:644
    installed_commit=$(<"$RUNTIME_ROOT/.solardt-installed-commit")
    [[ $installed_commit =~ ^[0-9a-f]{40}$ ]]
    verify_regular_metadata "$STATE_ROOT" "$SERVICE_USER:$SERVICE_GROUP:750"
    verify_regular_metadata "$EVIDENCE_ROOT" "$SERVICE_USER:$SERVICE_GROUP:750"
    verify_regular_metadata "$UNIT_DEST" root:root:644
    [[ ! -e /etc/systemd/system/timers.target.wants/esp32-forensic-collector.timer ]]
    [[ ! -e /etc/systemd/system/multi-user.target.wants/$UNIT_NAME ]]
    ! systemctl is-active --quiet "$UNIT_NAME"
    unit_state=$(systemctl is-enabled "$UNIT_NAME" 2>&1 || true)
    [[ $unit_state =~ ^(static|disabled)$ ]]
    ! runuser -u "$SERVICE_USER" -- test -w "$RUNTIME_ROOT"
    runuser -u "$SERVICE_USER" -- test -w "$EVIDENCE_ROOT"
    if [[ -n $reporter ]]; then
        getent passwd "$reporter" >/dev/null
        id -nG "$reporter" | tr ' ' '\n' | grep -Fxq "$SERVICE_GROUP"
        runuser -u "$reporter" -- test -r "$EVIDENCE_ROOT"
        ! runuser -u "$reporter" -- test -w "$EVIDENCE_ROOT"
    fi
    ! grep -Eq '^(EnvironmentFile|LoadCredential)=' "$UNIT_DEST"
    ! grep -Eq '^\[Install\]$' "$UNIT_DEST"
    echo "VERIFY: ESP32 runtime metadata passed; unit is dormant and no device was contacted"
}

validate_existing_runtime() {
    local accept_legacy=$1
    [[ ! -L $RUNTIME_ROOT && -d $RUNTIME_ROOT ]]
    [[ $(stat -c '%U:%G' "$RUNTIME_ROOT") == root:root ]]
    [[ -f $RUNTIME_ROOT/pyproject.toml && ! -L $RUNTIME_ROOT/pyproject.toml ]]
    [[ -f $RUNTIME_ROOT/requirements.txt && ! -L $RUNTIME_ROOT/requirements.txt ]]
    [[ -d $RUNTIME_ROOT/src/solar_digital_twin && ! -L $RUNTIME_ROOT/src/solar_digital_twin ]]
    [[ -d $RUNTIME_ROOT/.venv && ! -L $RUNTIME_ROOT/.venv ]]
    if [[ -e $RUNTIME_ROOT/.solardt-installed-commit ]]; then
        verify_regular_metadata "$RUNTIME_ROOT/.solardt-installed-commit" root:root:644
        grep -Eq '^[0-9a-f]{40}$' "$RUNTIME_ROOT/.solardt-installed-commit"
    elif [[ $accept_legacy -ne 1 ]]; then
        echo "ERROR: existing shared runtime lacks an installation marker; inspect it and rerun only with --accept-legacy-runtime" >&2
        exit 1
    fi
}

install_runtime() {
    local accept_legacy=$1 reporter=$2
    require_root
    require_clean_approved_source
    command -v systemctl >/dev/null
    ! systemctl is-active --quiet "$UNIT_NAME" || {
        echo "ERROR: existing ESP32 unit is active; refusing installation" >&2
        exit 1
    }

    if [[ -e $RUNTIME_ROOT ]]; then
        validate_existing_runtime "$accept_legacy"
    fi
    if [[ -e $UNIT_DEST ]]; then
        [[ ! -L $UNIT_DEST && -f $UNIT_DEST ]]
        [[ $(stat -c '%U:%G:%a' "$UNIT_DEST") == root:root:644 ]]
    fi
    if [[ -e /var/lib/solar-digital-twin ]]; then
        verify_regular_metadata /var/lib/solar-digital-twin root:root:755
        [[ -d /var/lib/solar-digital-twin ]]
    fi
    if [[ -e $STATE_ROOT ]]; then
        verify_regular_metadata "$STATE_ROOT" "$SERVICE_USER:$SERVICE_GROUP:750"
        [[ -d $STATE_ROOT ]]
    fi
    if [[ -e $EVIDENCE_ROOT ]]; then
        verify_regular_metadata "$EVIDENCE_ROOT" "$SERVICE_USER:$SERVICE_GROUP:750"
        [[ -d $EVIDENCE_ROOT ]]
    fi

    if getent group "$SERVICE_GROUP" >/dev/null; then
        [[ $(getent group "$SERVICE_GROUP" | cut -d: -f3) -lt 1000 ]]
    else
        groupadd --system "$SERVICE_GROUP"
    fi
    if getent passwd "$SERVICE_USER" >/dev/null; then
        verify_identity
    else
        useradd --system --gid "$SERVICE_GROUP" --no-create-home \
            --home-dir /nonexistent --shell /usr/sbin/nologin "$SERVICE_USER"
    fi
    if [[ -n $reporter ]]; then
        getent passwd "$reporter" >/dev/null
        usermod --append --groups "$SERVICE_GROUP" "$reporter"
    fi

    create_or_verify_directory /var/lib/solar-digital-twin root root 755
    create_or_verify_directory "$STATE_ROOT" "$SERVICE_USER" "$SERVICE_GROUP" 750
    create_or_verify_directory "$EVIDENCE_ROOT" "$SERVICE_USER" "$SERVICE_GROUP" 750

    source_commit=$(git -C "$REPO_ROOT" rev-parse HEAD)
    if (
        [[ -f $RUNTIME_ROOT/.solardt-installed-commit ]] &&
        [[ $(<"$RUNTIME_ROOT/.solardt-installed-commit") == "$source_commit" ]] &&
        [[ -f $UNIT_DEST && ! -L $UNIT_DEST ]] &&
        cmp -s -- "$REPO_ROOT/$UNIT_SOURCE" "$UNIT_DEST"
    ); then
        verify_metadata "$reporter"
        echo "INSTALL: exact approved ESP32 runtime state already present; no replacement performed"
        return
    fi

    stamp=$(date -u +%Y%m%dT%H%M%SZ)
    stage=/opt/.solar-digital-twin.new.$$
    runtime_backup=
    unit_backup=
    install -d -o root -g root -m 0755 "$stage"
    cleanup_stage() { [[ ! -e $stage ]] || rm -rf -- "$stage"; }
    trap cleanup_stage EXIT
    git -C "$REPO_ROOT" archive --format=tar HEAD | tar -x -C "$stage"
    python3 -m venv "$stage/.venv"
    "$stage/.venv/bin/pip" install --requirement "$stage/requirements.txt"
    "$stage/.venv/bin/pip" install "$stage"
    printf '%s\n' "$source_commit" >"$stage/.solardt-installed-commit"
    chown -R root:root "$stage"
    chmod -R u=rwX,go=rX "$stage"

    if [[ -e $RUNTIME_ROOT ]]; then
        runtime_backup=/opt/solar-digital-twin.backup.$stamp
        [[ ! -e $runtime_backup ]]
        mv -- "$RUNTIME_ROOT" "$runtime_backup"
    fi
    if [[ -e $UNIT_DEST ]]; then
        unit_backup=$UNIT_DEST.backup.$stamp
        cp --preserve=mode,ownership,timestamps -- "$UNIT_DEST" "$unit_backup"
    fi

    rollback_install() {
        status=$?
        if [[ $status -ne 0 ]]; then
            failed=/opt/solar-digital-twin.failed.$stamp
            [[ ! -e $RUNTIME_ROOT ]] || mv -- "$RUNTIME_ROOT" "$failed"
            [[ -z $runtime_backup ]] || mv -- "$runtime_backup" "$RUNTIME_ROOT"
            if [[ -n $unit_backup ]]; then
                cp --preserve=mode,ownership,timestamps -- "$unit_backup" "$UNIT_DEST"
            else
                [[ ! -e $UNIT_DEST ]] || mv -- "$UNIT_DEST" "$UNIT_DEST.failed.$stamp"
            fi
            systemctl daemon-reload || true
            echo "ERROR: installation failed; prior runtime restored and failed material preserved" >&2
        fi
        return "$status"
    }
    trap rollback_install EXIT
    mv -- "$stage" "$RUNTIME_ROOT"
    install -o root -g root -m 0644 "$REPO_ROOT/$UNIT_SOURCE" "$UNIT_DEST"
    systemctl daemon-reload
    ! systemctl is-active --quiet "$UNIT_NAME"
    unit_state=$(systemctl is-enabled "$UNIT_NAME" 2>&1 || true)
    [[ $unit_state =~ ^(static|disabled)$ ]]
    trap - EXIT

    echo "Installed ESP32 runtime and dormant unit; no service was started or enabled"
    [[ -z $runtime_backup ]] || echo "Previous shared runtime preserved at $runtime_backup"
    echo "No credential was created and no device was contacted"
}

mode=${1-}
shift || true
reporter=
accept_legacy=0
while [[ $# -gt 0 ]]; do
    case $1 in
        --reporter)
            [[ $# -ge 2 && -n $2 ]] || { usage >&2; exit 2; }
            reporter=$2
            shift 2
            ;;
        --accept-legacy-runtime)
            accept_legacy=1
            shift
            ;;
        *) usage >&2; exit 2 ;;
    esac
done

case $mode in
    --check)
        [[ -z $reporter && $accept_legacy -eq 0 ]] || { usage >&2; exit 2; }
        check_source
        ;;
    --install)
        install_runtime "$accept_legacy" "$reporter"
        ;;
    --verify)
        [[ $accept_legacy -eq 0 ]] || { usage >&2; exit 2; }
        verify_metadata "$reporter"
        ;;
    *) usage >&2; exit 2 ;;
esac
