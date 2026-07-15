import csv
from dataclasses import dataclass
from datetime import datetime, timezone, tzinfo
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo

REPORTS_DIR = Path("reports")
OUTPUT_FILE = REPORTS_DIR / "eg4_portal.html"
LOCAL_TZ = ZoneInfo("America/Chicago")
RUNTIME_MAX_AGE_MINUTES = 30
ENERGY_MAX_AGE_MINUTES = 30
DAY_TELEMETRY_MAX_AGE_MINUTES = 30


@dataclass(frozen=True)
class SourceHealth:
    state: str
    timestamp: datetime | None = None
    age_minutes: float | None = None

    @property
    def is_fresh(self) -> bool:
        return self.state == "Fresh"

    @property
    def timestamp_text(self) -> str:
        if self.timestamp is None:
            return "n/a"
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")

    @property
    def age_text(self) -> str:
        if self.age_minutes is None:
            return "n/a"
        if self.age_minutes < 0:
            return f"{abs(self.age_minutes):.1f} minutes in future"
        if self.age_minutes < 120:
            return f"{self.age_minutes:.1f} minutes old"
        return f"{self.age_minutes / 60:.1f} hours old"


def read_csv(filename: str) -> list[dict[str, str]]:
    path = REPORTS_DIR / filename
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def field(row: dict[str, str], key: str) -> str:
    value = (row.get(key) or "").strip()
    return value if value else "n/a"


def as_float(row: dict[str, str], key: str) -> float | None:
    value = (row.get(key) or "").strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def fmt_num(value: float | None, suffix: str = "") -> str:
    if value is None:
        return "n/a"
    if abs(value) >= 100:
        return f"{value:,.0f}{suffix}"
    return f"{value:,.1f}{suffix}"


def source_health(
    rows: list[dict[str, str]],
    key: str,
    source_tz: tzinfo,
    now: datetime,
    max_age_minutes: float,
) -> SourceHealth:
    if not rows:
        return SourceHealth("Missing")

    value = (rows[-1].get(key) or "").strip()
    if not value:
        return SourceHealth("Missing")

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return SourceHealth("Invalid timestamp")

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=source_tz)
    parsed = parsed.astimezone(LOCAL_TZ)
    age_minutes = (now - parsed).total_seconds() / 60

    if age_minutes < 0:
        state = "Future-dated"
    elif age_minutes <= max_age_minutes:
        state = "Fresh"
    else:
        state = "Stale"
    return SourceHealth(state, parsed, age_minutes)


def html(value: object) -> str:
    return escape(str(value))


def status_class(status: str) -> str:
    if status.lower() == "normal":
        return "ok"
    if status == "n/a":
        return "warn"
    return "alert"


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def percent(value: float | None, maximum: float) -> float:
    if value is None or maximum <= 0:
        return 0.0
    return clamp((value / maximum) * 100, 0, 100)


def metric_card(
    title: str,
    value: str,
    detail: str = "",
    value_class: str = "",
) -> str:
    detail_html = f"<div class='detail'>{html(detail)}</div>" if detail else ""
    class_text = f"value {value_class}".strip()
    return (
        "<section class='card'>"
        f"<h2>{html(title)}</h2>"
        f"<div class='{class_text}'>{html(value)}</div>"
        f"{detail_html}"
        "</section>"
    )


def gauge_card(
    title: str,
    value: float | None,
    maximum: float,
    suffix: str,
    detail: str = "",
) -> str:
    pct = percent(value, maximum)
    label = fmt_num(value, suffix)
    return (
        "<section class='card gauge-card'>"
        f"<h2>{html(title)}</h2>"
        f"<div class='gauge'><div style='width:{pct:.0f}%'></div></div>"
        f"<div class='value'>{html(label)}</div>"
        f"<div class='detail'>{html(detail or f'Scale: 0 to {fmt_num(maximum, suffix)}')}</div>"
        "</section>"
    )


def engineering_findings() -> list[str]:
    path = REPORTS_DIR / "engineering_daily_report.md"
    if not path.exists():
        return ["Engineering report not found."]

    lines = path.read_text(encoding="utf-8").splitlines()
    findings: list[str] = []
    in_section = False

    for line in lines:
        if line.startswith("## Engineering Findings"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.strip().startswith("- "):
            findings.append(line.strip()[2:])

    return findings or ["No engineering findings found."]


def health_class(state: str) -> str:
    if state == "Fresh":
        return "ok"
    if state in {"Stale", "Missing", "Invalid timestamp", "Future-dated"}:
        return "warn"
    return "alert"


def source_health_section(sources: list[tuple[str, SourceHealth]]) -> str:
    rows = "".join(
        "<tr>"
        f"<th scope='row'>{html(name)}</th>"
        f"<td class='{health_class(health.state)}'>{html(health.state)}</td>"
        f"<td>{html(health.timestamp_text)}</td>"
        f"<td>{html(health.age_text)}</td>"
        "</tr>"
        for name, health in sources
    )
    return (
        "<section class='card source-health'>"
        "<h2>EG4 Source Health</h2>"
        "<table><thead><tr><th>Source</th><th>State</th>"
        "<th>Latest observation</th><th>Approximate age</th></tr></thead>"
        f"<tbody>{rows}</tbody></table></section>"
    )


CSS = """
body{font-family:Arial,sans-serif;margin:0;background:#111827;color:#f9fafb}
main{max-width:1100px;margin:auto;padding:24px}
header{margin-bottom:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}
.card{background:#1f2937;border:1px solid #374151;border-radius:14px;padding:18px}
.card h2{font-size:15px;margin:0 0 12px;color:#cbd5e1}
.value{font-size:30px;font-weight:700}
.detail{color:#9ca3af;margin-top:8px;font-size:13px}
.gauge{height:18px;background:#374151;border-radius:999px;overflow:hidden}
.gauge div{height:100%;background:#38bdf8}
.ok{color:#22c55e}.warn{color:#f59e0b}.alert{color:#ef4444}
li{margin:8px 0}
.source-health{margin-top:16px;overflow-x:auto}
table{width:100%;border-collapse:collapse;text-align:left}
th,td{padding:9px;border-bottom:1px solid #374151;white-space:nowrap}
thead th{color:#cbd5e1;font-size:13px}
"""


def build_portal(now: datetime | None = None) -> str:
    now = now or datetime.now(LOCAL_TZ)
    runtime_rows = read_csv("runtime_snapshots.csv")
    energy_rows = read_csv("energy_snapshots.csv")
    day_rows = read_csv("day_multiline_samples.csv")
    runtime = runtime_rows[-1] if runtime_rows else {}
    energy = energy_rows[-1] if energy_rows else {}
    day = day_rows[-1] if day_rows else {}

    runtime_health = source_health(
        runtime_rows,
        "server_time",
        timezone.utc,
        now,
        RUNTIME_MAX_AGE_MINUTES,
    )
    energy_health = source_health(
        energy_rows,
        "server_time",
        timezone.utc,
        now,
        ENERGY_MAX_AGE_MINUTES,
    )
    day_health = source_health(
        day_rows,
        "sample_time",
        LOCAL_TZ,
        now,
        DAY_TELEMETRY_MAX_AGE_MINUTES,
    )

    status = field(runtime, "status_text") if runtime_health.is_fresh else "n/a"
    status_style = status_class(status) if runtime_health.is_fresh else "warn"
    runtime_detail = (
        f"Firmware: {field(runtime, 'fw_code')}; "
        f"Runtime observation: {runtime_health.timestamp_text}"
        if runtime_health.is_fresh
        else f"Runtime data unavailable: {runtime_health.state}"
    )
    soc = as_float(runtime, "soc") if runtime_health.is_fresh else None
    soc_detail = (
        "EG4 inverter estimate. Trusted Battery SOC (JK BMS via "
        "SolarAssistant) is already collected by the project but is not yet "
        "integrated into this portal. " + runtime_detail
    )
    today_usage = (
        as_float(energy, "today_usage_kwh") if energy_health.is_fresh else None
    )
    energy_detail = (
        f"Energy observation: {energy_health.timestamp_text}"
        if energy_health.is_fresh
        else f"Energy data unavailable: {energy_health.state}"
    )
    ac_power = as_float(day, "ac_couple_power_w") if day_health.is_fresh else None
    load = as_float(day, "consumption_w") if day_health.is_fresh else None
    day_detail = (
        f"Day observation: {day_health.timestamp_text}"
        if day_health.is_fresh
        else f"Day telemetry unavailable: {day_health.state}"
    )

    findings = "".join(
        f"<li>{html(item)}</li>" for item in engineering_findings()
    )

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate, max-age=0">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>EG4 Local Portal</title>
<style>{CSS}</style>
<script>
setTimeout(() => {{
    const url = new URL(window.location.href);
    url.searchParams.set("_refresh", Date.now().toString());
    window.location.replace(url.toString());
}}, 60000);
</script>
</head>
<body>
<main>
<header>
<h1>EG4 Local Portal</h1>
<p>Portal generated: {html(now.isoformat(timespec="seconds"))}</p>
</header>
<div class="grid">
{metric_card("System Status", status, runtime_detail, status_style)}
{gauge_card("EG4 Estimated SOC", soc, 100, "%", soc_detail)}
{gauge_card("AC-couple Power", ac_power, 5400, " W", day_detail)}
{gauge_card("Load", load, 12000, " W", day_detail)}
{metric_card("Today Usage", fmt_num(today_usage, " kWh"), energy_detail)}
</div>
{source_health_section([
    ("Runtime", runtime_health),
    ("Energy", energy_health),
    ("Day Telemetry", day_health),
])}
<section class="card">
<h2>Latest Engineering Findings</h2>
<ul>{findings}</ul>
</section>
</main>
</body>
</html>
"""


def write_portal() -> Path:
    REPORTS_DIR.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(build_portal(), encoding="utf-8")
    return OUTPUT_FILE


def main() -> int:
    path = write_portal()
    print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
