"""Install approved integration credentials without exposing secret values."""

from __future__ import annotations

import argparse
import getpass
import grp
import os
import pwd
import re
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol


SecretReader = Callable[[str], str]
ConfirmationReader = Callable[[str], str]


@dataclass(frozen=True)
class EnvironmentSetting:
    name: str

    def validate(self) -> None:
        if not _SETTING_NAME.fullmatch(self.name):
            raise CredentialInstallError("credential setting name is unsafe")

    def encode(self, secret: str) -> bytes:
        escaped = secret.replace("\\", "\\\\").replace('"', '\\"')
        return f'{self.name}="{escaped}"\n'.encode("utf-8")


class CredentialPayload(Protocol):
    def validate(self) -> None: ...

    def encode(self, secret: str) -> bytes: ...


@dataclass(frozen=True)
class CredentialProfile:
    identifier: str
    destination: Path
    allowed_directory: Path
    owner: str
    group: str
    mode: int
    payload: CredentialPayload
    prompt: str


SOLARASSISTANT = CredentialProfile(
    identifier="solarassistant",
    destination=Path("/etc/solar-digital-twin/solarassistant.env"),
    allowed_directory=Path("/etc/solar-digital-twin"),
    owner="root",
    group="root",
    mode=0o600,
    payload=EnvironmentSetting("SOLARASSISTANT_PASSWORD"),
    prompt="SolarAssistant password: ",
)

PROFILES = {SOLARASSISTANT.identifier: SOLARASSISTANT}
_SETTING_NAME = re.compile(r"^[A-Z][A-Z0-9_]*$")


class CredentialInstallError(Exception):
    """A safe, non-secret credential installation error."""


def _validate_profile(profile: CredentialProfile) -> None:
    destination = profile.destination
    allowed_directory = profile.allowed_directory
    if not destination.is_absolute() or not allowed_directory.is_absolute():
        raise CredentialInstallError("credential paths must be absolute")
    if ".." in destination.parts or ".." in allowed_directory.parts:
        raise CredentialInstallError("credential paths must not contain parent traversal")
    if destination.parent != allowed_directory:
        raise CredentialInstallError("credential destination is outside its approved directory")
    if destination.name in {"", ".", ".."}:
        raise CredentialInstallError("credential destination is unsafe")
    if profile.mode != 0o600:
        raise CredentialInstallError("credential file permissions must be 0600")
    profile.payload.validate()


def _prepare_directory(path: Path, uid: int, gid: int) -> None:
    try:
        info = path.lstat()
    except FileNotFoundError:
        path.mkdir(mode=0o700, parents=False)
        path.chmod(0o700)
        os.chown(path, uid, gid)
        return

    if not stat.S_ISDIR(info.st_mode) or path.is_symlink():
        raise CredentialInstallError("approved credential directory is not a safe directory")
    if info.st_uid != uid or info.st_gid != gid:
        raise CredentialInstallError("approved credential directory has unexpected ownership")
    if info.st_mode & 0o022:
        raise CredentialInstallError("approved credential directory is group- or world-writable")


def _validate_existing_destination(path: Path) -> bool:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return False
    if not stat.S_ISREG(info.st_mode) or path.is_symlink():
        raise CredentialInstallError("credential destination is not a regular file")
    return True


def _encode_secret(profile: CredentialProfile, secret: str) -> bytes:
    if not secret:
        raise CredentialInstallError("secret input must not be empty")
    if any(ord(character) < 32 or ord(character) == 127 for character in secret):
        raise CredentialInstallError("secret input contains unsupported control characters")
    return profile.payload.encode(secret)


def install_profile(
    profile: CredentialProfile,
    *,
    secret_reader: SecretReader = getpass.getpass,
    confirmation_reader: ConfirmationReader = input,
) -> Path:
    """Install one validated profile and return only its destination path."""
    _validate_profile(profile)
    uid = pwd.getpwnam(profile.owner).pw_uid
    gid = grp.getgrnam(profile.group).gr_gid

    _prepare_directory(profile.allowed_directory, uid, gid)
    replacing = _validate_existing_destination(profile.destination)
    if replacing:
        answer = confirmation_reader(
            f"Credential file already exists for {profile.identifier}. "
            "Type REPLACE to replace it: "
        )
        if answer != "REPLACE":
            raise CredentialInstallError("existing credential file was not replaced")

    secret = secret_reader(profile.prompt)
    confirmation = secret_reader("Confirm secret: ")
    if secret != confirmation:
        raise CredentialInstallError("secret confirmation did not match")
    content = _encode_secret(profile, secret)

    descriptor = -1
    temporary_name: str | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{profile.destination.name}.",
            dir=profile.allowed_directory,
        )
        os.fchmod(descriptor, profile.mode)
        os.fchown(descriptor, uid, gid)
        with os.fdopen(descriptor, "wb", closefd=True) as credential_file:
            descriptor = -1
            credential_file.write(content)
            credential_file.flush()
            os.fsync(credential_file.fileno())
        os.replace(temporary_name, profile.destination)
        temporary_name = None
        directory_fd = os.open(profile.allowed_directory, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if temporary_name is not None:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass

    return profile.destination


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("service", help="approved service identifier")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    profile = PROFILES.get(args.service)
    if profile is None:
        raise SystemExit(f"Unknown credential service profile: {args.service}")
    if os.geteuid() != 0:
        raise SystemExit("Credential installation must run as root.")

    try:
        destination = install_profile(profile)
    except CredentialInstallError as exc:
        raise SystemExit(f"Credential installation failed: {exc}") from None

    print(
        f"Installed {profile.identifier} credential at {destination} "
        f"with owner {profile.owner}:{profile.group} and mode {profile.mode:04o}."
    )


if __name__ == "__main__":
    main()
