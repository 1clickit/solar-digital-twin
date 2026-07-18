#!/usr/bin/env python3
"""Coordinate isolated ESP32, EG4, and SolarAssistant forensic captures."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import pwd
import re
import shlex
import shutil
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, TextIO
from zoneinfo import ZoneInfo

import yaml


CAPTURE_SCHEMA = "solar-digital-twin.coordinated-capture.v1"
DEFAULT_DURATION = 86_400.0
DEFAULT_EG4_INTERVAL = 900.0
LOCK_PATH = Path("/run/solar-digital-twin/coordinated-capture.lock")
CAPTURE_ID_RE = re.compile(r"^solar-forensic-[0-9]{8}T[0-9]{6}Z$")
RELEVANT_UNITS = (
    "eg4-refresh-report.timer",
    "eg4-refresh-report.service",
    "eg4-local-portal.service",
)
STOPPED_FOR_CAPTURE = (
    "eg4-refresh-report.timer",
    "eg4-refresh-report.service",
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_text(value: datetime | None = None) -> str:
    return (value or utc_now()).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


def local_text(value: datetime) -> str:
    return value.astimezone(ZoneInfo("America/Chicago")).isoformat(
        timespec="seconds"
    )


def default_capture_id(value: datetime | None = None) -> str:
    return f"solar-forensic-{(value or utc_now()).strftime('%Y%m%dT%H%M%SZ')}"


def append_manifest(handle: TextIO, event: str, **fields: Any) -> None:
    payload = {
        "schema": CAPTURE_SCHEMA,
        "event": event,
        "recorded_at_utc": utc_text(),
        **fields,
    }
    handle.write(json.dumps(payload, separators=(",", ":")) + "\n")
    handle.flush()


def cleanup_manifest_event(handle: TextIO, event: str, **fields: Any) -> bool:
    """Best-effort lifecycle recording that never prevents cleanup/restoration."""
    try:
        append_manifest(handle, event, **fields)
    except OSError:
        return False
    return True


def command_result(command: list[str]) -> tuple[int, str]:
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode, completed.stdout.strip()


def unit_state(unit: str) -> dict[str, str]:
    _, loaded = command_result(
        ["systemctl", "show", unit, "--property=LoadState", "--value"]
    )
    active_rc, active = command_result(["systemctl", "is-active", unit])
    enabled_rc, enabled = command_result(["systemctl", "is-enabled", unit])
    return {
        "unit": unit,
        "loaded": loaded or "unknown",
        "active": active if active_rc in {0, 3} else "unknown",
        "enabled": enabled if enabled_rc in {0, 1} else "unknown",
    }


def stop_units(prior: list[dict[str, str]], manifest: TextIO) -> None:
    by_name = {item["unit"]: item for item in prior}
    for unit in STOPPED_FOR_CAPTURE:
        if by_name.get(unit, {}).get("active") != "active":
            continue
        completed = subprocess.run(
            ["systemctl", "stop", unit], check=False, capture_output=True
        )
        append_manifest(
            manifest,
            "prior_unit_stopped",
            unit=unit,
            success=completed.returncode == 0,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"could not stop competing unit: {unit}")


def restore_units(prior: list[dict[str, str]], manifest: TextIO) -> bool:
    success = True
    by_name = {item["unit"]: item for item in prior}
    for unit in reversed(STOPPED_FOR_CAPTURE):
        if by_name.get(unit, {}).get("active") != "active":
            continue
        completed = subprocess.run(
            ["systemctl", "start", unit], check=False, capture_output=True
        )
        restored = completed.returncode == 0
        success = success and restored
        cleanup_manifest_event(
            manifest,
            "prior_unit_restored",
            unit=unit,
            success=restored,
        )
    return success


def load_environment_file(path: Path) -> dict[str, str]:
    """Load a narrow systemd-style environment file without logging values."""
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError("invalid credential environment file")
        key, raw_value = line.split("=", 1)
        if key not in {"EG4_USERNAME", "EG4_PASSWORD"}:
            continue
        parsed = shlex.split(raw_value, posix=True)
        if len(parsed) != 1:
            raise ValueError("invalid credential environment value")
        values[key] = parsed[0]
    if set(values) != {"EG4_USERNAME", "EG4_PASSWORD"}:
        raise ValueError("required EG4 credential variables are unavailable")
    return values


def safe_child_environment(extra: dict[str, str] | None = None) -> dict[str, str]:
    environment = {
        "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "LANG": os.environ.get("LANG", "C.UTF-8"),
        "HOME": "/home/chris",
    }
    environment.update(extra or {})
    return environment


def run_as(user: str, command: list[str], group: str | None = None) -> list[str]:
    prefix = ["/usr/sbin/runuser", "--preserve-environment", "-u", user]
    if group is not None:
        prefix.extend(["-g", group])
    return [*prefix, "--", *command]


@dataclass
class Child:
    source: str
    process: subprocess.Popen[bytes]
    log_handle: TextIO
    command_summary: list[str]


def terminate_children(children: list[Child], manifest: TextIO) -> None:
    for child in children:
        if child.process.poll() is None:
            os.killpg(child.process.pid, signal.SIGTERM)
    deadline = time.monotonic() + 45.0
    for child in children:
        remaining = max(0.0, deadline - time.monotonic())
        try:
            child.process.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            os.killpg(child.process.pid, signal.SIGKILL)
            child.process.wait(timeout=10)
        cleanup_manifest_event(
            manifest,
            "source_stopped",
            source=child.source,
            pid=child.process.pid,
            returncode=child.process.returncode,
        )
        child.log_handle.close()


def create_source_dirs(run_dir: Path) -> dict[str, Path]:
    users = {"esp32": "chris", "eg4": "chris", "solarassistant": "solardt-sa"}
    reader_group = pwd.getpwnam("chris").pw_gid
    paths: dict[str, Path] = {}
    for source, user in users.items():
        path = run_dir / source
        path.mkdir(mode=0o750)
        account = pwd.getpwnam(user)
        os.chown(path, account.pw_uid, reader_group)
        paths[source] = path
    return paths


def write_eg4_config(repo: Path, source_dir: Path) -> Path:
    base = yaml.safe_load((repo / "config/eg4.yaml").read_text(encoding="utf-8"))
    config = {
        "serial": base["serial"],
        "database": str(source_dir / "eg4_capture.sqlite"),
        "evidence_dir": str(source_dir / "evidence"),
        "reports_dir": str(source_dir / "reports"),
    }
    path = source_dir / "capture_config.yaml"
    path.write_text(yaml.safe_dump(config, sort_keys=True), encoding="utf-8")
    account = pwd.getpwnam("chris")
    os.chown(path, account.pw_uid, account.pw_gid)
    return path


def launch_child(
    source: str,
    command: list[str],
    log_path: Path,
    manifest: TextIO,
    environment: dict[str, str] | None = None,
) -> Child:
    log_handle = log_path.open("x", encoding="utf-8")
    process = subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        env=environment,
        start_new_session=True,
    )
    summary = [part for part in command if "PASSWORD" not in part]
    try:
        append_manifest(
            manifest,
            "source_started",
            source=source,
            pid=process.pid,
            started_at_utc=utc_text(),
            command=summary,
        )
    except BaseException:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=10)
        log_handle.close()
        raise
    return Child(source, process, log_handle, summary)


def artifacts_ready(paths: dict[str, Path]) -> dict[str, bool]:
    return {
        "esp32": len(list(paths["esp32"].glob("esp32_sse_*.ndjson"))) >= 4,
        "solarassistant": len(
            list(paths["solarassistant"].glob("solarassistant_*.ndjson"))
        )
        >= 2,
        "eg4": (paths["eg4"] / "eg4_capture.sqlite").exists()
        and any((paths["eg4"] / "evidence").glob("*/*.json")),
    }


def verify_startup(
    children: list[Child],
    paths: dict[str, Path],
    manifest: TextIO,
    timeout: float,
) -> None:
    deadline = time.monotonic() + timeout
    latest: dict[str, bool] = {}
    while time.monotonic() < deadline:
        exited = [child.source for child in children if child.process.poll() is not None]
        if exited:
            raise RuntimeError(f"source exited during startup: {','.join(exited)}")
        latest = artifacts_ready(paths)
        if all(latest.values()):
            append_manifest(manifest, "startup_verified", sources=latest)
            return
        time.sleep(2.0)
    raise RuntimeError(f"startup artifacts incomplete: {latest}")


def acquire_lock() -> TextIO:
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    handle = LOCK_PATH.open("a+", encoding="utf-8")
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as exc:
        handle.close()
        raise RuntimeError("another coordinated capture holds the lock") from exc
    return handle


def run_live(args: argparse.Namespace) -> int:
    if os.geteuid() != 0:
        raise RuntimeError("live coordination must run as root")
    if not CAPTURE_ID_RE.fullmatch(args.capture_id):
        raise ValueError("invalid capture identifier")

    repo = args.repo.resolve()
    lock = acquire_lock()
    run_dir = args.capture_root.resolve() / args.capture_id
    run_dir.mkdir(parents=True, exist_ok=False, mode=0o755)
    manifest_path = run_dir / "coordinated_manifest.ndjson"
    manifest = manifest_path.open("x", encoding="utf-8", buffering=1)
    children: list[Child] = []
    prior = [unit_state(unit) for unit in RELEVANT_UNITS]
    started = utc_now()
    planned_end = started + timedelta(seconds=args.duration)
    stop_requested = False
    terminal = "failure"
    reason = "startup_failure"

    def request_stop(_signum: int, _frame: Any) -> None:
        nonlocal stop_requested, reason
        stop_requested = True
        reason = "signal"

    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)

    try:
        source_dirs = create_source_dirs(run_dir)
        eg4_config = write_eg4_config(repo, source_dirs["eg4"])
        append_manifest(
            manifest,
            "capture_started",
            capture_id=args.capture_id,
            repository_commit=args.commit,
            hostname=os.uname().nodename,
            planned_duration_seconds=args.duration,
            actual_start_utc=utc_text(started),
            planned_end_utc=utc_text(planned_end),
            actual_start_local=local_text(started),
            planned_end_local=local_text(planned_end),
            prior_units=prior,
            source_interfaces={
                "esp32": "read-only SSE",
                "eg4": "read-only cloud telemetry",
                "solarassistant": "read-only /api/v1/metrics",
            },
            retention_policies=["esp32-frequency-v1", "esp32-conservative-v1"],
            output_directory=str(run_dir),
        )

        stop_units(prior, manifest)
        eg4_credentials = load_environment_file(args.eg4_environment_file)
        python = str(repo / ".venv/bin/python")
        eg4_command = run_as(
            "chris",
            [
                python,
                str(Path(__file__).resolve()),
                "eg4-loop",
                "--repo",
                str(repo),
                "--config",
                str(eg4_config),
                "--duration",
                str(args.duration),
                "--interval",
                str(args.eg4_interval),
            ],
        )
        solar_command = run_as(
            "solardt-sa",
            [
                "/opt/solar-digital-twin/.venv/bin/python",
                "-m",
                "solar_digital_twin.collectors.solarassistant",
                "--password-file",
                str(args.solarassistant_password_file),
                "--output-dir",
                str(source_dirs["solarassistant"]),
                "--interval",
                "10",
                "--duration",
                str(args.duration),
            ],
            group="chris",
        )
        esp32_command = run_as(
            "chris",
            [
                python,
                "-m",
                "solar_digital_twin.collectors.esp32_sse",
                "--output-dir",
                str(source_dirs["esp32"]),
                "--retention-mode",
                "canary",
                "--collector-version",
                args.commit,
                "--duration",
                str(args.duration),
            ],
        )

        children.append(
            launch_child(
                "eg4",
                eg4_command,
                source_dirs["eg4"] / "collector.log",
                manifest,
                safe_child_environment(eg4_credentials),
            )
        )
        children.append(
            launch_child(
                "solarassistant",
                solar_command,
                source_dirs["solarassistant"] / "collector.log",
                manifest,
                safe_child_environment(),
            )
        )
        children.append(
            launch_child(
                "esp32",
                esp32_command,
                source_dirs["esp32"] / "collector.log",
                manifest,
                safe_child_environment(),
            )
        )
        verify_startup(children, source_dirs, manifest, args.startup_timeout)
        terminal = "completion"
        reason = "duration"

        deadline = time.monotonic() + max(
            0.0, args.duration - (utc_now() - started).total_seconds()
        )
        observed_exits: set[str] = set()
        while time.monotonic() < deadline and not stop_requested:
            for child in children:
                if child.process.poll() is not None and child.source not in observed_exits:
                    observed_exits.add(child.source)
                    append_manifest(
                        manifest,
                        "source_exited_early",
                        source=child.source,
                        returncode=child.process.returncode,
                    )
                    terminal = "failure"
                    reason = f"source_exit:{child.source}"
                    stop_requested = True
            free_bytes = shutil.disk_usage(run_dir).free
            if free_bytes < args.minimum_free_bytes:
                append_manifest(
                    manifest,
                    "controlled_stop",
                    reason="free_space_threshold",
                    free_bytes=free_bytes,
                )
                terminal = "failure"
                reason = "free_space_threshold"
                stop_requested = True
            time.sleep(min(5.0, max(0.0, deadline - time.monotonic())))
        if stop_requested and reason == "signal":
            terminal = "interruption"
    except BaseException as exc:
        append_manifest(manifest, "capture_error", error_type=type(exc).__name__)
        raise
    finally:
        terminate_children(children, manifest)
        restoration_ok = restore_units(prior, manifest)
        try:
            append_manifest(
                manifest,
                "capture_terminal",
                state=terminal,
                reason=reason,
                actual_end_utc=utc_text(),
                restoration_success=restoration_ok,
            )
        finally:
            manifest.close()
            lock.close()
    return 0 if terminal == "completion" and restoration_ok else 1


def run_eg4_loop(args: argparse.Namespace) -> int:
    deadline = time.monotonic() + args.duration
    stop = False

    def request_stop(_signum: int, _frame: Any) -> None:
        nonlocal stop
        stop = True

    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    while not stop and time.monotonic() < deadline:
        local_date = datetime.now(ZoneInfo("America/Chicago")).strftime("%Y-%m-%d")
        process = subprocess.Popen(
            [
                str(args.repo / ".venv/bin/python"),
                str(args.repo / "src/solar_digital_twin/collectors/eg4/eg4_sync.py"),
                "--config",
                str(args.config),
                "--date",
                local_date,
                "--skip-set-records",
            ],
            cwd=args.repo,
        )
        while process.poll() is None and not stop:
            time.sleep(0.5)
        if stop and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)
        if process.returncode != 0:
            print(f"EG4 isolated sync failed with exit {process.returncode}", flush=True)
        remaining = deadline - time.monotonic()
        if remaining <= 0 or stop:
            break
        sleep_until = time.monotonic() + min(args.interval, remaining)
        while not stop and time.monotonic() < sleep_until:
            time.sleep(min(1.0, sleep_until - time.monotonic()))
    return 0


def run_rehearsal(args: argparse.Namespace) -> int:
    capture_id = args.capture_id or default_capture_id()
    run_dir = args.output_dir / capture_id
    run_dir.mkdir(parents=True, exist_ok=False)
    manifest_path = run_dir / "coordinated_manifest.ndjson"
    children: list[subprocess.Popen[bytes]] = []
    started = utc_now()
    with manifest_path.open("x", encoding="utf-8", buffering=1) as manifest:
        append_manifest(
            manifest,
            "capture_started",
            capture_id=capture_id,
            synthetic=True,
            actual_start_utc=utc_text(started),
            planned_end_utc=utc_text(started + timedelta(seconds=args.duration)),
        )
        try:
            for source in ("esp32", "eg4", "solarassistant"):
                source_dir = run_dir / source
                source_dir.mkdir()
                artifact = source_dir / "synthetic.ndjson"
                code = (
                    "import pathlib,time;"
                    f"p=pathlib.Path({str(artifact)!r});"
                    "p.write_text('{\"synthetic\":true}\\n');"
                    f"time.sleep({args.duration})"
                )
                process = subprocess.Popen([sys.executable, "-c", code])
                children.append(process)
                append_manifest(manifest, "source_started", source=source, pid=process.pid)
            time.sleep(args.duration)
            append_manifest(manifest, "startup_verified", synthetic=True)
        finally:
            for process in children:
                if process.poll() is None:
                    process.terminate()
                process.wait(timeout=5)
            append_manifest(manifest, "capture_terminal", state="completion", synthetic=True)
    print(json.dumps({"capture_id": capture_id, "run_dir": str(run_dir)}))
    return 0


def status(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    manifest_path = run_dir / "coordinated_manifest.ndjson"
    events = [json.loads(line) for line in manifest_path.read_text().splitlines()]
    start = next(item for item in events if item["event"] == "capture_started")
    last = events[-1]
    source_starts = {
        item["source"]: item
        for item in events
        if item["event"] == "source_started"
    }
    sizes: dict[str, int] = {}
    for source in ("esp32", "eg4", "solarassistant"):
        source_dir = run_dir / source
        sizes[source] = sum(
            path.stat().st_size for path in source_dir.rglob("*") if path.is_file()
        )
    now = utc_now()
    started = datetime.fromisoformat(start["actual_start_utc"].replace("Z", "+00:00"))
    planned_end_value = start.get("planned_end_utc")
    planned_end = (
        datetime.fromisoformat(planned_end_value.replace("Z", "+00:00"))
        if planned_end_value
        else None
    )
    process_state: dict[str, str] = {}
    for source, item in source_starts.items():
        try:
            os.kill(int(item["pid"]), 0)
        except (OSError, ValueError):
            process_state[source] = "not-running"
        else:
            process_state[source] = "running"
    recent_errors: dict[str, str] = {}
    for source in ("esp32", "eg4", "solarassistant"):
        log = run_dir / source / "collector.log"
        if not log.exists():
            continue
        with log.open("rb") as handle:
            handle.seek(0, os.SEEK_END)
            length = handle.tell()
            handle.seek(max(0, length - 8192))
            lines = handle.read().decode("utf-8", errors="replace").splitlines()[-20:]
        errors = [line[:240] for line in lines if "error" in line.lower() or "failed" in line.lower()]
        if errors:
            recent_errors[source] = errors[-1]
    output = {
        "capture_id": start["capture_id"],
        "elapsed_seconds": round((now - started).total_seconds(), 1),
        "remaining_seconds": (
            max(0.0, round((planned_end - now).total_seconds(), 1))
            if planned_end
            else None
        ),
        "planned_end_utc": planned_end_value,
        "manifest_state": last["event"],
        "process_state": process_state,
        "source_bytes": sizes,
        "free_bytes": shutil.disk_usage(run_dir).free,
        "recent_errors": recent_errors,
    }
    print(json.dumps(output, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)

    live = sub.add_parser("live", help="Run the approved live coordinator as root.")
    live.add_argument("--capture-id", required=True)
    live.add_argument("--capture-root", type=Path, required=True)
    live.add_argument("--repo", type=Path, required=True)
    live.add_argument("--commit", required=True)
    live.add_argument("--duration", type=float, default=DEFAULT_DURATION)
    live.add_argument("--eg4-interval", type=float, default=DEFAULT_EG4_INTERVAL)
    live.add_argument("--startup-timeout", type=float, default=300.0)
    live.add_argument("--minimum-free-bytes", type=int, default=5 * 1024**3)
    live.add_argument("--eg4-environment-file", type=Path, required=True)
    live.add_argument("--solarassistant-password-file", type=Path, required=True)
    live.set_defaults(handler=run_live)

    eg4 = sub.add_parser("eg4-loop")
    eg4.add_argument("--repo", type=Path, required=True)
    eg4.add_argument("--config", type=Path, required=True)
    eg4.add_argument("--duration", type=float, required=True)
    eg4.add_argument("--interval", type=float, required=True)
    eg4.set_defaults(handler=run_eg4_loop)

    rehearsal = sub.add_parser("rehearse")
    rehearsal.add_argument("--output-dir", type=Path, required=True)
    rehearsal.add_argument("--capture-id")
    rehearsal.add_argument("--duration", type=float, default=0.2)
    rehearsal.set_defaults(handler=run_rehearsal)

    show = sub.add_parser("status")
    show.add_argument("--run-dir", type=Path, required=True)
    show.set_defaults(handler=status)
    return result


def main() -> None:
    args = parser().parse_args()
    try:
        raise SystemExit(args.handler(args))
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"Coordinated capture error: {exc}", file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
