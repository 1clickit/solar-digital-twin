import os
import pwd
import grp
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from solar_digital_twin.credentials import (
    CredentialInstallError,
    CredentialProfile,
    EnvironmentSetting,
    PROFILES,
    SOLARASSISTANT,
    install_profile,
    main,
)


class CredentialInstallerTests(unittest.TestCase):
    def profile(self, root: Path) -> CredentialProfile:
        return CredentialProfile(
            identifier="test-profile",
            destination=root / "credentials" / "test.env",
            allowed_directory=root / "credentials",
            owner=pwd.getpwuid(os.getuid()).pw_name,
            group=grp.getgrgid(os.getgid()).gr_name,
            mode=0o600,
            payload=EnvironmentSetting("TEST_SECRET"),
            prompt="Secret: ",
        )

    def test_only_solarassistant_is_registered(self):
        self.assertEqual(PROFILES, {"solarassistant": SOLARASSISTANT})
        self.assertEqual(
            SOLARASSISTANT.destination,
            Path("/etc/solar-digital-twin/solarassistant.env"),
        )
        self.assertEqual(SOLARASSISTANT.owner, "root")
        self.assertEqual(SOLARASSISTANT.group, "root")
        self.assertEqual(SOLARASSISTANT.mode, 0o600)
        self.assertEqual(
            SOLARASSISTANT.payload,
            EnvironmentSetting("SOLARASSISTANT_PASSWORD"),
        )

    def test_installs_hidden_confirmed_secret_with_secure_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            profile = self.profile(Path(directory))
            prompts = []

            def read_secret(prompt):
                prompts.append(prompt)
                return 'secret with $ and "quotes"'

            destination = install_profile(profile, secret_reader=read_secret)

            self.assertEqual(destination, profile.destination)
            self.assertEqual(len(prompts), 2)
            self.assertEqual(stat.S_IMODE(destination.stat().st_mode), 0o600)
            self.assertEqual(
                destination.read_text(encoding="utf-8"),
                'TEST_SECRET="secret with $ and \\"quotes\\""\n',
            )

    def test_refuses_empty_and_mismatched_input_without_creating_file(self):
        for answers in (("", ""), ("first", "second")):
            with self.subTest(answers=answers), tempfile.TemporaryDirectory() as directory:
                profile = self.profile(Path(directory))
                responses = iter(answers)
                with self.assertRaises(CredentialInstallError):
                    install_profile(profile, secret_reader=lambda _: next(responses))
                self.assertFalse(profile.destination.exists())

    def test_requires_explicit_confirmation_before_atomic_replacement(self):
        with tempfile.TemporaryDirectory() as directory:
            profile = self.profile(Path(directory))
            profile.allowed_directory.mkdir(mode=0o700)
            profile.destination.write_text("original\n", encoding="utf-8")
            profile.destination.chmod(0o600)

            with self.assertRaises(CredentialInstallError):
                install_profile(
                    profile,
                    secret_reader=lambda _: "replacement",
                    confirmation_reader=lambda _: "no",
                )
            self.assertEqual(profile.destination.read_text(encoding="utf-8"), "original\n")

            install_profile(
                profile,
                secret_reader=lambda _: "replacement",
                confirmation_reader=lambda _: "REPLACE",
            )
            self.assertEqual(
                profile.destination.read_text(encoding="utf-8"),
                'TEST_SECRET="replacement"\n',
            )
            self.assertEqual(list(profile.allowed_directory.glob(".test.env.*")), [])

    def test_refuses_destination_outside_approved_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profile = self.profile(root)
            unsafe = CredentialProfile(
                **{**profile.__dict__, "destination": root / "elsewhere.env"}
            )
            with self.assertRaises(CredentialInstallError):
                install_profile(unsafe, secret_reader=lambda _: "secret")

    def test_refuses_unsafe_existing_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            profile = self.profile(Path(directory))
            profile.allowed_directory.mkdir(mode=0o777)
            profile.allowed_directory.chmod(0o777)
            with self.assertRaises(CredentialInstallError):
                install_profile(profile, secret_reader=lambda _: "secret")

    def test_refuses_unknown_service_profile(self):
        with patch.object(sys, "argv", ["credentials", "unknown"]):
            with self.assertRaisesRegex(SystemExit, "Unknown credential service profile"):
                main()


if __name__ == "__main__":
    unittest.main()
