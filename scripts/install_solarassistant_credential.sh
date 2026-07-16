#!/usr/bin/env bash

set -euo pipefail

SERVICE_GROUP=solardt-sa
CREDENTIAL_ROOT=/etc/solar-digital-twin/solarassistant
PASSWORD_FILE=$CREDENTIAL_ROOT/password

usage() {
    echo "Usage: $0 [--check]"
}

check_design() {
    command -v install >/dev/null
    command -v mktemp >/dev/null
    command -v stty >/dev/null
    command -v sync >/dev/null
    echo "CHECK: fixed credential destination is $PASSWORD_FILE"
    echo "CHECK: no password argument is accepted and no system path was changed"
}

install_credential() {
    if [[ $# -ne 0 ]]; then
        usage >&2
        exit 2
    fi
    if [[ $EUID -ne 0 ]]; then
        echo "ERROR: administrator privilege is required" >&2
        exit 1
    fi
    if ! exec 3<>/dev/tty; then
        echo "ERROR: a controlling terminal is required" >&2
        exit 1
    fi
    [[ $(stat -c '%U:%G:%a' "$CREDENTIAL_ROOT") == "root:$SERVICE_GROUP:750" ]] || {
        echo "ERROR: credential directory metadata is not approved" >&2
        exit 1
    }
    [[ ! -L $CREDENTIAL_ROOT ]] || {
        echo "ERROR: credential directory must not be a symlink" >&2
        exit 1
    }

    password=
    confirmation=
    temporary=
    cleanup() {
        stty echo <&3 2>/dev/null || true
        password=
        confirmation=
        [[ -z $temporary ]] || rm -f -- "$temporary"
    }
    trap cleanup EXIT HUP INT TERM

    printf 'SolarAssistant password: ' >&3
    stty -echo <&3
    IFS= read -r password <&3
    printf '\nConfirm SolarAssistant password: ' >&3
    IFS= read -r confirmation <&3
    stty echo <&3
    printf '\n' >&3

    [[ -n $password && -n ${password//[[:space:]]/} ]] || {
        echo "ERROR: password cannot be empty" >&2
        exit 1
    }
    [[ $password == "$confirmation" ]] || {
        echo "ERROR: password confirmation did not match" >&2
        exit 1
    }

    umask 077
    temporary=$(mktemp "$CREDENTIAL_ROOT/.password.new.XXXXXX")
    printf '%s\n' "$password" > "$temporary"
    chown root:"$SERVICE_GROUP" "$temporary"
    chmod 0640 "$temporary"
    sync -f "$temporary"
    [[ $(stat -c '%U:%G:%a' "$temporary") == "root:$SERVICE_GROUP:640" ]]
    mv -fT -- "$temporary" "$PASSWORD_FILE"
    temporary=
    sync -f "$CREDENTIAL_ROOT"
    password=
    confirmation=
    echo "SolarAssistant credential installed with approved metadata"
    echo "One separately approved manual verification is required before automation resumes"
}

case ${1-} in
    --check)
        [[ $# -eq 1 ]] || { usage >&2; exit 2; }
        check_design
        ;;
    "")
        install_credential
        ;;
    *)
        usage >&2
        exit 2
        ;;
esac
