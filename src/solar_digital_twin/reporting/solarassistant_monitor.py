"""LAN-oriented, read-only live monitor for SolarAssistant NDJSON evidence."""

from __future__ import annotations

import argparse
import html
import json
import math
import os
import secrets
import signal
import threading
import time
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


DEFAULT_EVIDENCE_DIR = Path("/var/lib/solar-digital-twin/solarassistant/evidence")
DEFAULT_BIND = "127.0.0.1"
DEFAULT_PORT = 8792
DEFAULT_CAPTURE_DURATION = 86_400.0
DEFAULT_FRESHNESS_SECONDS = 30.0
SNAPSHOT_COMPLETION_DELAY = 0.75
COLLECTOR_MODULE = "solar_digital_twin.collectors.solarassistant"

GROUPS = {
    "Combined": "total/",
    "Battery 1": "battery_1/",
    "Battery 2": "battery_2/",
}
PROMINENT_SUFFIXES = (
    "state_of_charge", "voltage", "current", "power", "state_of_health",
    "temperature", "cell_voltage_-_average", "cell_voltage_-_highest",
    "cell_voltage_-_lowest", "cell_voltage_-_imbalance",
)
SECONDARY_SUFFIXES = (
    "capacity", "charge_capacity", "cycles", "temperature_1",
    "temperature_2", "temperature_mos",
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def numeric_value(value: Any) -> Decimal | None:
    if isinstance(value, bool):
        return None
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None
    return result if result.is_finite() else None


def is_retained(path: Path) -> bool:
    return path.name.endswith("_retained.ndjson")


def newest_raw_file(evidence_dir: Path) -> Path | None:
    try:
        candidates = [
            path for path in evidence_dir.glob("solarassistant_*.ndjson")
            if path.is_file() and not is_retained(path)
        ]
    except OSError:
        return None
    dated = []
    for path in candidates:
        try:
            dated.append((path.stat().st_mtime_ns, path.name, path))
        except OSError:
            continue
    return max(dated, default=(0, "", None))[2]


def validate_raw_file(evidence_dir: Path, raw_file: Path) -> Path:
    if is_retained(raw_file):
        raise ValueError("a retained NDJSON file cannot be used as raw evidence")
    root = evidence_dir.resolve()
    candidate = raw_file.resolve()
    if not candidate.is_relative_to(root):
        raise ValueError("--raw-file must reside inside --evidence-dir")
    if not candidate.is_file():
        raise ValueError("--raw-file must name an existing regular file")
    return candidate


def retained_sibling(raw_file: Path | None) -> Path | None:
    if raw_file is None:
        return None
    return raw_file.with_name(f"{raw_file.stem}_retained{raw_file.suffix}")


def topic_group(topic: str) -> str | None:
    for label, prefix in GROUPS.items():
        if topic.startswith(prefix):
            return label
    return None


def topic_suffix(topic: str) -> str:
    suffix = topic.split("/", 1)[1] if "/" in topic else topic
    if topic.startswith("total/battery_"):
        suffix = suffix.removeprefix("battery_")
    if suffix == "cell_imbalance_-_average":
        return "cell_voltage_-_imbalance"
    return suffix


def format_duration(seconds: float) -> str:
    total = max(0, int(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


class MonitorState:
    """Thread-safe in-memory state derived from append-only raw evidence."""

    def __init__(
        self,
        evidence_dir: Path,
        raw_file: Path | None,
        capture_duration: float,
        freshness_seconds: float,
        clock: Callable[[], datetime] = utc_now,
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        self.evidence_dir = evidence_dir
        self.raw_file = raw_file
        self.capture_duration = capture_duration
        self.freshness_seconds = freshness_seconds
        self.clock = clock
        self.monotonic = monotonic
        self.lock = threading.RLock()
        self.latest_by_identity: dict[tuple[Any, ...], dict[str, Any]] = {}
        self.latest_snapshot: dict[str, dict[str, Any]] = {}
        self.numeric_ranges: dict[str, list[Decimal]] = {}
        self.raw_record_count = 0
        self.poll_count = 0
        self.invalid_record_count = 0
        self.retained_record_count = 0
        self.retained_offset = 0
        self.first_receipt: datetime | None = None
        self.latest_receipt: datetime | None = None
        self.last_update: datetime | None = None
        self.gaps: list[dict[str, Any]] = []
        self._pending_timestamp: str | None = None
        self._pending_records: dict[str, dict[str, Any]] = {}
        self._pending_since = 0.0
        self.stopping = False
        self.stop_requested_at: datetime | None = None
        self.collector_seen = False
        self.collector_identity: ProcessIdentity | None = None
        self.collector_reason = "Collector process has not been inspected yet."

    def set_raw_file(self, path: Path) -> None:
        with self.lock:
            self.raw_file = path

    def ingest_complete_line(self, line: bytes) -> None:
        try:
            record = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            with self.lock:
                self.invalid_record_count += 1
            return
        if not isinstance(record, dict):
            with self.lock:
                self.invalid_record_count += 1
            return
        timestamp = record.get("received_at_utc")
        topic = record.get("topic")
        if parse_timestamp(timestamp) is None or not isinstance(topic, str):
            with self.lock:
                self.invalid_record_count += 1
            return
        with self.lock:
            if self._pending_timestamp is not None and timestamp != self._pending_timestamp:
                self._publish_pending()
            if self._pending_timestamp is None:
                self._pending_timestamp = timestamp
                self._pending_since = self.monotonic()
            self._pending_records[topic] = record
            self._observe(record)

    def _observe(self, record: dict[str, Any]) -> None:
        identity = tuple(record.get(key) for key in ("topic", "device", "number", "group", "name", "unit"))
        self.latest_by_identity[identity] = record
        self.raw_record_count += 1
        number = numeric_value(record.get("value"))
        if number is not None:
            topic = record["topic"]
            bounds = self.numeric_ranges.setdefault(topic, [number, number])
            bounds[0] = min(bounds[0], number)
            bounds[1] = max(bounds[1], number)

    def _publish_pending(self) -> None:
        if self._pending_timestamp is None:
            return
        receipt = parse_timestamp(self._pending_timestamp)
        if receipt is not None:
            if self.latest_receipt is not None:
                gap = (receipt - self.latest_receipt).total_seconds()
                threshold = max(20.0, self.freshness_seconds)
                if gap > threshold:
                    self.gaps.append({"from": self.latest_receipt.isoformat(), "to": receipt.isoformat(), "seconds": gap})
            self.first_receipt = self.first_receipt or receipt
            self.latest_receipt = receipt
        self.latest_snapshot = dict(self._pending_records)
        self.poll_count += 1
        self.last_update = self.clock()
        self._pending_timestamp = None
        self._pending_records = {}
        self._pending_since = 0.0

    def flush_pending(self, force: bool = False) -> bool:
        with self.lock:
            due = self._pending_timestamp is not None and (
                force or self.monotonic() - self._pending_since >= SNAPSHOT_COMPLETION_DELAY
            )
            if due:
                self._publish_pending()
            return due

    def bootstrap(self) -> int:
        path = self.raw_file
        if path is None:
            return 0
        offset = 0
        try:
            with path.open("rb") as handle:
                while True:
                    line_start = handle.tell()
                    line = handle.readline()
                    if not line:
                        offset = handle.tell()
                        break
                    if not line.endswith(b"\n"):
                        offset = line_start
                        break
                    self.ingest_complete_line(line)
                    offset = handle.tell()
        except OSError:
            return 0
        self.flush_pending(force=True)
        self.bootstrap_retained()
        return offset

    def bootstrap_retained(self) -> None:
        path = retained_sibling(self.raw_file)
        count = 0
        offset = 0
        if path is not None:
            try:
                with path.open("rb") as handle:
                    while True:
                        start = handle.tell()
                        line = handle.readline()
                        if not line:
                            offset = handle.tell()
                            break
                        if not line.endswith(b"\n"):
                            offset = start
                            break
                        count += 1
                        offset = handle.tell()
            except OSError:
                pass
        with self.lock:
            self.retained_record_count = count
            self.retained_offset = offset

    def update_retained_count(self) -> None:
        path = retained_sibling(self.raw_file)
        if path is None:
            return
        added = 0
        try:
            with path.open("rb") as handle:
                handle.seek(self.retained_offset)
                while True:
                    start = handle.tell()
                    line = handle.readline()
                    if not line:
                        self.retained_offset = handle.tell()
                        break
                    if not line.endswith(b"\n"):
                        self.retained_offset = start
                        break
                    added += 1
                    self.retained_offset = handle.tell()
        except OSError:
            return
        with self.lock:
            self.retained_record_count += added

    def countdown(self, now: datetime | None = None) -> dict[str, Any]:
        now = now or self.clock()
        start = self.first_receipt
        if start is None:
            return {"elapsed_seconds": 0.0, "remaining_seconds": self.capture_duration,
                    "elapsed": "00:00:00", "remaining": format_duration(self.capture_duration),
                    "expected_end": None, "progress_percent": 0.0, "stopped_early": False}
        expected = start + timedelta(seconds=self.capture_duration)
        elapsed = max(0.0, (now - start).total_seconds())
        remaining = max(0.0, self.capture_duration - elapsed)
        collector_gone = self.collector_identity is None and self.collector_seen
        return {
            "elapsed_seconds": elapsed,
            "remaining_seconds": remaining,
            "elapsed": format_duration(elapsed),
            "remaining": format_duration(remaining),
            "expected_end": expected.isoformat(),
            "progress_percent": min(100.0, (elapsed / self.capture_duration * 100.0) if self.capture_duration else 100.0),
            "stopped_early": collector_gone and remaining > 0,
        }

    def status_dict(self, include_token: str | None = None) -> dict[str, Any]:
        with self.lock:
            now = self.clock()
            countdown = self.countdown(now)
            age = None if self.latest_receipt is None else max(0.0, (now - self.latest_receipt).total_seconds())
            if countdown["remaining_seconds"] <= 0:
                capture_status = "Complete"
            elif self.stopping:
                capture_status = "Stopping"
            elif countdown["stopped_early"]:
                capture_status = "Stopped"
            elif self.latest_receipt is None:
                capture_status = "Unknown"
            elif age is not None and age > self.freshness_seconds:
                capture_status = "Stale"
            elif self.collector_identity is not None:
                capture_status = "Fresh"
            else:
                capture_status = "Running"
            raw_size = _safe_size(self.raw_file)
            retained = retained_sibling(self.raw_file)
            result = {
                "capture_status": capture_status,
                "data_freshness": "Waiting" if age is None else ("Fresh" if age <= self.freshness_seconds else "Stale"),
                "data_age_seconds": age,
                "latest_receipt": _iso(self.latest_receipt),
                "first_receipt": _iso(self.first_receipt),
                "raw_filename": None if self.raw_file is None else self.raw_file.name,
                "retained_filename": None if retained is None else retained.name,
                "raw_record_count": self.raw_record_count,
                "retained_record_count": self.retained_record_count,
                "poll_count": self.poll_count,
                "invalid_record_count": self.invalid_record_count,
                "raw_file_size": raw_size,
                "countdown": countdown,
                "capture_start": _iso(self.first_receipt),
                "assembling_newer_poll": self._pending_timestamp is not None,
                "groups": grouped_snapshot(self.latest_snapshot),
                "numeric_ranges": {topic: {"minimum": _decimal_text(bounds[0]), "maximum": _decimal_text(bounds[1])}
                                   for topic, bounds in sorted(self.numeric_ranges.items())},
                "gaps": list(self.gaps),
                "abort_enabled": self.collector_identity is not None and not self.stopping,
                "abort_reason": self.collector_reason,
            }
            if include_token is not None:
                result["control_token"] = include_token
            return result


def _iso(value: datetime | None) -> str | None:
    return None if value is None else value.isoformat()


def _decimal_text(value: Decimal) -> str:
    return format(value, "f")


def _safe_size(path: Path | None) -> int:
    if path is None:
        return 0
    try:
        return path.stat().st_size
    except OSError:
        return 0


def grouped_snapshot(snapshot: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {name: {} for name in GROUPS}
    for topic, record in snapshot.items():
        group = topic_group(topic)
        if group is not None:
            groups[group][topic_suffix(topic)] = {
                "value": record.get("value"), "unit": record.get("unit"),
                "received_at_utc": record.get("received_at_utc"), "name": record.get("name"),
            }
    return groups


class EvidenceTailer(threading.Thread):
    def __init__(self, state: MonitorState, stop_event: threading.Event, poll_seconds: float = 0.2) -> None:
        super().__init__(name="solarassistant-evidence-tailer", daemon=True)
        self.state = state
        self.stop_event = stop_event
        self.poll_seconds = poll_seconds
        self.offset = 0

    def run(self) -> None:
        while not self.stop_event.is_set():
            if self.state.raw_file is None:
                selected = newest_raw_file(self.state.evidence_dir)
                if selected is not None:
                    self.state.set_raw_file(selected)
                    self.offset = self.state.bootstrap()
            else:
                self._read_growth()
                self.state.update_retained_count()
            self.state.flush_pending()
            self.stop_event.wait(self.poll_seconds)

    def _read_growth(self) -> None:
        path = self.state.raw_file
        if path is None:
            return
        try:
            with path.open("rb") as handle:
                handle.seek(self.offset)
                while True:
                    start = handle.tell()
                    line = handle.readline()
                    if not line:
                        self.offset = handle.tell()
                        return
                    if not line.endswith(b"\n"):
                        self.offset = start
                        return
                    self.state.ingest_complete_line(line)
                    self.offset = handle.tell()
        except OSError:
            return


class ProcessIdentity:
    def __init__(self, pid: int, uid: int, start_ticks: str, command: tuple[str, ...]) -> None:
        self.pid, self.uid, self.start_ticks, self.command = pid, uid, start_ticks, command


def inspect_process(pid: int, proc_root: Path = Path("/proc")) -> ProcessIdentity | None:
    base = proc_root / str(pid)
    try:
        uid = base.stat().st_uid
        command = tuple(part.decode("utf-8", "replace") for part in base.joinpath("cmdline").read_bytes().split(b"\0") if part)
        stat_text = base.joinpath("stat").read_text(encoding="utf-8")
        fields = stat_text[stat_text.rfind(")") + 2:].split()
        start_ticks = fields[19]
    except (OSError, IndexError):
        return None
    return ProcessIdentity(pid, uid, start_ticks, command)


def command_matches(identity: ProcessIdentity, evidence_dir: Path, own_pid: int) -> bool:
    command = identity.command
    module_match = any(command[index:index + 2] == ("-m", COLLECTOR_MODULE) for index in range(len(command) - 1))
    return identity.pid != own_pid and module_match and str(evidence_dir) in command


def discover_collector(evidence_dir: Path, uid: int | None = None, proc_root: Path = Path("/proc"), own_pid: int | None = None) -> tuple[ProcessIdentity | None, str]:
    uid = os.getuid() if uid is None else uid
    own_pid = os.getpid() if own_pid is None else own_pid
    matches = []
    try:
        entries = list(proc_root.iterdir())
    except OSError:
        return None, "Process information is unavailable; Abort Capture is disabled."
    for entry in entries:
        if not entry.name.isdigit():
            continue
        identity = inspect_process(int(entry.name), proc_root)
        if identity is not None and identity.uid == uid and command_matches(identity, evidence_dir, own_pid):
            matches.append(identity)
    if not matches:
        return None, "No uniquely identifiable collector process was found; Abort Capture is disabled."
    if len(matches) > 1:
        return None, "More than one matching collector process was found; Abort Capture is disabled."
    return matches[0], "Exactly one same-UID collector process is safely identified."


class AbortController:
    def __init__(self, state: MonitorState, proc_root: Path = Path("/proc"), kill: Callable[[int, int], None] = os.kill) -> None:
        self.state, self.proc_root, self.kill = state, proc_root, kill

    def refresh(self) -> None:
        identity, reason = discover_collector(self.state.evidence_dir, proc_root=self.proc_root)
        with self.state.lock:
            previous = self.state.collector_identity
            self.state.collector_identity, self.state.collector_reason = identity, reason
            if identity is not None:
                self.state.collector_seen = True
            elif previous is not None and self.state.stop_requested_at is None:
                self.state.stop_requested_at = self.state.clock()
            if self.state.stopping and identity is None:
                self.state.stopping = False

    def abort(self) -> tuple[bool, str]:
        with self.state.lock:
            expected = self.state.collector_identity
        if expected is None:
            return False, "No safely identified collector is available to stop."
        current = inspect_process(expected.pid, self.proc_root)
        if current is None or current.uid != os.getuid() or current.start_ticks != expected.start_ticks or current.command != expected.command or not command_matches(current, self.state.evidence_dir, os.getpid()):
            with self.state.lock:
                self.state.collector_identity = None
                self.state.collector_reason = "Collector process identity changed; Abort Capture was refused."
            return False, "Collector process identity changed; no signal was sent."
        try:
            self.kill(expected.pid, signal.SIGTERM)
        except OSError:
            return False, "The collector exited before the stop request could be delivered."
        with self.state.lock:
            self.state.stopping = True
            self.state.stop_requested_at = self.state.clock()
            self.state.collector_reason = "SIGTERM was sent once; waiting for clean collector shutdown."
        return True, "Stop request accepted; existing evidence is preserved."


def render_dashboard() -> str:
    return r"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>SolarAssistant Live Capture</title><style>
:root{color-scheme:dark;--bg:#0b1220;--panel:#152033;--line:#2d3c55;--text:#eef4ff;--muted:#aab8ce;--ok:#48d597;--warn:#ffc857;--danger:#ff6b6b}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px system-ui,sans-serif}main{max-width:1500px;margin:auto;padding:20px}.header{display:flex;gap:20px;justify-content:space-between;align-items:flex-start}.status{display:inline-block;padding:5px 10px;border-radius:99px;background:#263854}.controls,.section,.details{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px}.controls{min-width:320px}.countdown{font-size:2.2rem;font-weight:750}.bar{height:10px;background:#263854;border-radius:9px;overflow:hidden}.bar span{display:block;height:100%;background:var(--ok)}button,a.button{border:0;border-radius:8px;padding:10px 14px;margin:10px 6px 0 0;font-weight:700;cursor:pointer;text-decoration:none;display:inline-block}.report{background:#dce8ff;color:#10203a}.abort{background:var(--danger);color:#1b0808}.abort:disabled{opacity:.45;cursor:not-allowed}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:18px}.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.card{padding:12px;background:#101a2b;border-radius:10px}.card strong{display:block;font-size:1.35rem}.label,.muted{color:var(--muted)}table{width:100%;border-collapse:collapse;margin-top:10px}td,th{text-align:left;padding:7px;border-bottom:1px solid var(--line)}.details{margin-top:14px}.detail-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}@media(max-width:950px){.header{display:block}.controls{margin-top:14px}.grid{grid-template-columns:1fr}.detail-grid{grid-template-columns:repeat(2,1fr)}}
</style></head><body><main><div class='header'><div><h1>SolarAssistant Live Capture</h1><p><span id='status' class='status'>Unknown</span> Latest receipt: <span id='latest'>Waiting for data</span><br>Data age: <span id='age'>Waiting</span></p></div><section class='controls'><div class='muted'>Remaining</div><div id='remaining' class='countdown'>24:00:00</div><div id='stopped-note'></div><p>Elapsed: <span id='elapsed'>00:00:00</span><br>Expected completion: <span id='expected'>Waiting for data</span></p><div class='bar'><span id='progress' style='width:0%'></span></div><a class='button report' href='/report' target='_blank' rel='noopener'>Report</a><button id='abort' class='abort' disabled>Abort Capture</button><p id='abort-reason' class='muted'></p></section></div><div id='groups' class='grid'></div><section class='details'><h2>Capture details</h2><div id='details' class='detail-grid'></div></section></main>
<script>
let token='';const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const shown=v=>v===null||v===undefined||v===''?'Not reported':esc(v);const title=s=>s.replaceAll('_',' ').replace(/\b\w/g,c=>c.toUpperCase());
function card(name,row){let value=row?shown(row.value):'Waiting for data',unit=row&&row.unit?' '+esc(row.unit):'';return `<div class='card'><span class='label'>${title(name)}</span><strong>${value}${unit}</strong><small>${row?esc(row.received_at_utc):'Not reported'}</small></div>`}
function render(d){token=d.control_token||token;status.textContent=d.capture_status;latest.textContent=d.latest_receipt||'No capture data yet';age.textContent=d.data_age_seconds===null?'Waiting':`${Math.round(d.data_age_seconds)} seconds (${d.data_freshness})`;remaining.textContent=d.countdown.remaining;elapsed.textContent=d.countdown.elapsed;expected.textContent=d.countdown.expected_end||'Waiting for data';progress.style.width=`${d.countdown.progress_percent}%`;document.getElementById('stopped-note').textContent=d.countdown.stopped_early?`Capture stopped with ${d.countdown.remaining} remaining`:'';
groups.innerHTML=Object.entries(d.groups).map(([name,rows])=>{let primary=%PRIMARY%.map(k=>card(k,rows[k])).join('');let secondary=%SECONDARY%.map(k=>card(k,rows[k])).join('');return `<section class='section'><h2>${esc(name)}</h2><div class='cards'>${primary}${secondary}</div></section>`}).join('');
let detail={"Raw file":d.raw_filename,"Retained file":d.retained_filename,"Raw records":d.raw_record_count,"Retained records":d.retained_record_count,"Polls":d.poll_count,"Invalid lines":d.invalid_record_count,"Raw size":`${d.raw_file_size} bytes`,"Capture start":d.capture_start,"Latest poll":d.latest_receipt,"Expected completion":d.countdown.expected_end,"Freshness":d.data_freshness,"Newer poll":d.assembling_newer_poll?'Assembling':'No'};details.innerHTML=Object.entries(detail).map(([k,v])=>`<div><span class='label'>${esc(k)}</span><br><strong>${shown(v)}</strong></div>`).join('');abort.disabled=!d.abort_enabled;document.getElementById('abort-reason').textContent=d.abort_reason;}
async function update(){try{let r=await fetch('/api/status',{cache:'no-store'});render(await r.json())}catch(e){status.textContent='Unknown'}}setInterval(update,2000);update();
abort.onclick=async()=>{if(!confirm('Stop only the current capture? Evidence already written is preserved and no data is deleted.'))return;let r=await fetch('/api/abort',{method:'POST',headers:{'Content-Type':'application/json','X-Control-Token':token},body:'{}'});let d=await r.json();alert(d.message);update()};
</script></body></html>""".replace("%PRIMARY%", json.dumps(PROMINENT_SUFFIXES)).replace("%SECONDARY%", json.dumps(SECONDARY_SUFFIXES))


def render_report(data: dict[str, Any], generated: datetime | None = None) -> str:
    generated = generated or utc_now()
    rows = []
    for group, topics in data["groups"].items():
        for suffix in (*PROMINENT_SUFFIXES, *SECONDARY_SUFFIXES):
            record = topics.get(suffix, {})
            topic = next((key for key in data["numeric_ranges"] if topic_group(key) == group and topic_suffix(key) == suffix), None)
            bounds = data["numeric_ranges"].get(topic, {}) if topic else {}
            rows.append(f"<tr><td>{html.escape(group)}</td><td>{html.escape(suffix)}</td><td>{html.escape(str(record.get('value', 'Not reported')))}</td><td>{html.escape(str(record.get('unit') or ''))}</td><td>{html.escape(str(bounds.get('minimum', 'Not reported')))}</td><td>{html.escape(str(bounds.get('maximum', 'Not reported')))}</td></tr>")
    gaps = "No reliably observed gaps." if not data["gaps"] else "; ".join(f"{gap['seconds']:.1f}s from {gap['from']} to {gap['to']}" for gap in data["gaps"])
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>SolarAssistant Capture Report</title></head><body><h1>SolarAssistant Capture Report</h1><p>Generated: {html.escape(generated.isoformat())}</p><ul><li>Status: {html.escape(data['capture_status'])}</li><li>Elapsed / remaining: {html.escape(data['countdown']['elapsed'])} / {html.escape(data['countdown']['remaining'])}</li><li>Capture start / expected end: {html.escape(str(data['capture_start']))} / {html.escape(str(data['countdown']['expected_end']))}</li><li>Raw / retained file: {html.escape(str(data['raw_filename']))} / {html.escape(str(data['retained_filename']))}</li><li>Raw / retained records: {data['raw_record_count']} / {data['retained_record_count']}</li><li>Polls / invalid lines: {data['poll_count']} / {data['invalid_record_count']}</li><li>Earliest / latest receipt: {html.escape(str(data['first_receipt']))} / {html.escape(str(data['latest_receipt']))}</li><li>Data freshness: {html.escape(data['data_freshness'])}</li><li>Observed gaps: {html.escape(gaps)}</li></ul><table><thead><tr><th>Group</th><th>Metric</th><th>Current</th><th>Unit</th><th>Minimum</th><th>Maximum</th></tr></thead><tbody>{''.join(rows)}</tbody></table></body></html>"""


SECURITY_HEADERS = {
    "Cache-Control": "no-store",
    "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
}


class MonitorApplication:
    def __init__(self, state: MonitorState, abort_controller: AbortController, control_token: str | None = None) -> None:
        self.state = state
        self.abort_controller = abort_controller
        self.control_token = control_token or secrets.token_urlsafe(32)

    def handler_class(self) -> type[BaseHTTPRequestHandler]:
        application = self
        class Handler(BaseHTTPRequestHandler):
            def _send(self, status: int, body: bytes, content_type: str) -> None:
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                for key, value in SECURITY_HEADERS.items():
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(body)
            def _json(self, status: int, value: dict[str, Any]) -> None:
                self._send(status, json.dumps(value, separators=(",", ":")).encode(), "application/json; charset=utf-8")
            def do_GET(self) -> None:
                path = urlsplit(self.path).path
                if path == "/":
                    self._send(200, render_dashboard().encode(), "text/html; charset=utf-8")
                elif path == "/api/status":
                    self._json(200, application.state.status_dict(application.control_token))
                elif path == "/report":
                    self._send(200, render_report(application.state.status_dict()).encode(), "text/html; charset=utf-8")
                elif path == "/health":
                    self._json(200, {"status": "ok"})
                elif path == "/api/abort":
                    self._json(405, {"accepted": False, "message": "Abort requires POST."})
                else:
                    self._json(404, {"error": "not found"})
            def do_POST(self) -> None:
                if urlsplit(self.path).path != "/api/abort":
                    self._json(404, {"error": "not found"}); return
                origin = self.headers.get("Origin")
                expected_origin = f"http://{self.headers.get('Host', '')}"
                token = self.headers.get("X-Control-Token")
                if origin != expected_origin or not secrets.compare_digest(token or "", application.control_token):
                    self._json(403, {"accepted": False, "message": "Abort request was rejected."}); return
                accepted, message = application.abort_controller.abort()
                self._json(202 if accepted else 409, {"accepted": accepted, "message": message})
            def log_message(self, format: str, *args: Any) -> None:
                return
        return Handler


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, default=DEFAULT_EVIDENCE_DIR)
    parser.add_argument("--raw-file", type=Path)
    parser.add_argument("--bind", default=DEFAULT_BIND)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--capture-duration", type=float, default=DEFAULT_CAPTURE_DURATION)
    parser.add_argument("--freshness-seconds", type=float, default=DEFAULT_FRESHNESS_SECONDS)
    args = parser.parse_args(argv)
    if not 0 <= args.port <= 65535:
        parser.error("--port must be between 0 and 65535")
    if not math.isfinite(args.capture_duration) or args.capture_duration <= 0:
        parser.error("--capture-duration must be positive")
    if not math.isfinite(args.freshness_seconds) or args.freshness_seconds <= 0:
        parser.error("--freshness-seconds must be positive")
    if args.raw_file is not None:
        try:
            args.raw_file = validate_raw_file(args.evidence_dir, args.raw_file)
        except ValueError as exc:
            parser.error(str(exc))
    return args


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    raw_file = args.raw_file or newest_raw_file(args.evidence_dir)
    state = MonitorState(args.evidence_dir.resolve(), raw_file, args.capture_duration, args.freshness_seconds)
    stop_event = threading.Event()
    tailer = EvidenceTailer(state, stop_event)
    if raw_file is not None:
        tailer.offset = state.bootstrap()
    abort_controller = AbortController(state)
    application = MonitorApplication(state, abort_controller)
    server = ThreadingHTTPServer((args.bind, args.port), application.handler_class())
    tailer.start()
    print(f"SolarAssistant monitor: http://{args.bind}:{server.server_port}")
    print("Foreground process only; no service or daemon was created.")
    try:
        while True:
            abort_controller.refresh()
            server.timeout = 1.0
            server.handle_request()
    except KeyboardInterrupt:
        print("\nMonitor stopped; the collector was not stopped.")
    finally:
        stop_event.set()
        tailer.join(timeout=2)
        server.server_close()


if __name__ == "__main__":
    main()
