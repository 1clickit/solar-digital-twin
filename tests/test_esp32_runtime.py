import configparser
import shutil
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "scripts/install_esp32_runtime.sh"
LAUNCHER = REPO_ROOT / "scripts/run_esp32_forensic_collector.sh"
UNIT = REPO_ROOT / "systemd/esp32-forensic-collector.service"


class ESP32InstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = INSTALLER.read_text()

    def test_check_is_side_effect_free_and_reports_boundaries(self):
        before = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        result = subprocess.run(
            ["bash", str(INSTALLER), "--check"],
            cwd=REPO_ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        after = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        self.assertEqual(after, before)
        self.assertIn("no installation", result.stdout)
        self.assertIn("no device was contacted", result.stdout)
        self.assertNotIn("sudo", result.stdout)

    def test_dirty_and_untracked_source_are_detected(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            shutil.copy2(INSTALLER, root / "scripts/install_esp32_runtime.sh")
            required = (
                "requirements.txt",
                "pyproject.toml",
                "src/solar_digital_twin/collectors/esp32_sse.py",
                "src/solar_digital_twin/collectors/esp32_retention.py",
                "scripts/run_esp32_forensic_collector.sh",
                "systemd/esp32-forensic-collector.service",
            )
            for relative in required:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("placeholder\n")
            (root / "scripts/run_esp32_forensic_collector.sh").chmod(0o755)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(
                ["git", "remote", "add", "origin", "https://github.com/1clickit/solar-digital-twin.git"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                ["git", "add", ".", ":!scripts/run_esp32_forensic_collector.sh"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                [
                    "git", "-c", "user.name=Test", "-c",
                    "user.email=test@example.invalid", "commit", "-qm", "fixture",
                ],
                cwd=root,
                check=True,
            )
            (root / "requirements.txt").write_text("dirty\n")
            result = subprocess.run(
                ["bash", str(root / "scripts/install_esp32_runtime.sh"), "--check"],
                cwd=root,
                check=True,
                text=True,
                capture_output=True,
            )

        self.assertIn("working tree has changes; installation would refuse", result.stdout)
        self.assertIn("pending file must be committed", result.stdout)

    def test_identity_paths_and_no_credential_path(self):
        self.assertIn("SERVICE_USER=solardt-telemetry", self.source)
        self.assertIn("SERVICE_GROUP=solardt-telemetry", self.source)
        self.assertIn("RUNTIME_ROOT=/opt/solar-digital-twin", self.source)
        self.assertIn("STATE_ROOT=/var/lib/solar-digital-twin/esp32", self.source)
        self.assertNotIn("CREDENTIAL_ROOT=", self.source)
        self.assertIn("--no-create-home", self.source)
        self.assertIn("--shell /usr/sbin/nologin", self.source)

    def test_whole_tracked_runtime_archive_and_rollback_are_explicit(self):
        self.assertIn('git -C "$REPO_ROOT" archive --format=tar HEAD', self.source)
        self.assertIn(".solardt-installed-commit", self.source)
        self.assertIn("solar-digital-twin.backup.$stamp", self.source)
        self.assertIn("solar-digital-twin.failed.$stamp", self.source)
        self.assertIn("prior runtime restored", self.source)
        self.assertIn("--accept-legacy-runtime", self.source)

    def test_exact_installed_state_is_idempotent(self):
        self.assertIn("exact approved ESP32 runtime state already present", self.source)
        self.assertIn('cmp -s -- "$REPO_ROOT/$UNIT_SOURCE" "$UNIT_DEST"', self.source)
        self.assertIn('verify_metadata "$reporter"', self.source)

    def test_unknown_types_and_symlinks_are_refused(self):
        self.assertIn("[[ ! -L $RUNTIME_ROOT && -d $RUNTIME_ROOT ]]", self.source)
        self.assertIn("[[ ! -L $UNIT_DEST && -f $UNIT_DEST ]]", self.source)
        self.assertIn("required regular input is missing", self.source)
        self.assertNotIn("chown -R $SERVICE_USER", self.source)

    def test_install_and_verify_do_not_contact_device_or_start_service(self):
        self.assertNotIn("curl ", self.source)
        self.assertNotIn("wget ", self.source)
        self.assertNotIn("systemctl start", self.source)
        self.assertNotIn("systemctl enable", self.source)
        self.assertIn("systemctl is-active", self.source)
        self.assertIn("systemctl is-enabled", self.source)
        self.assertIn("--verify", self.source)

    def test_reporting_access_is_explicit_and_read_only(self):
        self.assertIn("--reporter", self.source)
        self.assertIn('test -r "$EVIDENCE_ROOT"', self.source)
        self.assertIn('! runuser -u "$reporter" -- test -w "$EVIDENCE_ROOT"', self.source)
        self.assertIn("usermod --append --groups", self.source)


class ESP32LauncherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = LAUNCHER.read_text()

    def test_launcher_is_fixed_finite_and_current_policy(self):
        self.assertIn("DURATION_SECONDS=3600", self.source)
        self.assertIn("--duration", self.source)
        self.assertIn("--retention-mode current", self.source)
        self.assertIn("--collector-version", self.source)
        self.assertIn("/var/lib/solar-digital-twin/esp32/evidence", self.source)
        self.assertNotIn("curl", self.source)
        self.assertNotIn("wget", self.source)


class ESP32SystemdUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = UNIT.read_text()
        cls.config = configparser.ConfigParser(interpolation=None, strict=True)
        cls.config.optionxform = str
        cls.config.read_string(cls.text)

    def test_unit_is_dormant_with_no_timer_or_install_target(self):
        self.assertNotIn("Install", self.config)
        self.assertNotIn(".timer", self.text)
        self.assertEqual(self.config["Service"]["Restart"], "no")
        self.assertNotIn("WantedBy", self.text)

    def test_unit_identity_duration_path_and_policy(self):
        service = self.config["Service"]
        self.assertEqual(service["User"], "solardt-telemetry")
        self.assertEqual(service["Group"], "solardt-telemetry")
        self.assertEqual(service["UMask"], "0027")
        self.assertEqual(service["Type"], "oneshot")
        self.assertIn("run_esp32_forensic_collector.sh", service["ExecStart"])
        launcher = LAUNCHER.read_text()
        self.assertIn("DURATION_SECONDS=3600", launcher)
        self.assertIn("--retention-mode current", launcher)

    def test_unit_hardening_and_writable_scope(self):
        service = self.config["Service"]
        expected = {
            "NoNewPrivileges": "true",
            "PrivateTmp": "true",
            "ProtectHome": "true",
            "ProtectSystem": "strict",
            "ReadWritePaths": "/var/lib/solar-digital-twin/esp32",
            "RestrictAddressFamilies": "AF_INET AF_UNIX",
        }
        for key, value in expected.items():
            self.assertEqual(service[key], value)
        self.assertNotIn("/opt/solar-digital-twin", service["ReadWritePaths"])

    def test_unit_is_credentialless_and_direct(self):
        service = self.config["Service"]
        self.assertNotIn("EnvironmentFile", service)
        self.assertNotIn("LoadCredential", service)
        self.assertNotIn("/bin/sh", service["ExecStart"])
        self.assertNotIn("|", service["ExecStart"])


if __name__ == "__main__":
    unittest.main()
