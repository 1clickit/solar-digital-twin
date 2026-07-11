import csv
from datetime import datetime, timezone, tzinfo
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo

REPORTS_DIR = Path("reports")
OUTPUT_FILE = REPORTS_DIR / "eg4_portal.html"
LOCAL_TZ = ZoneInfo("America/Chicago")
DAY_TELEMETRY_MAX_AGE_MINUTES = 30


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


def latest_datetime(
    rows: list[dict[str, str]], key: str, source_tz: tzinfo
) -> datetime | None:
    timestamps: list[datetime] = []
    for row in rows:
        value = field(row, key)
        if value == "n/a":
            continue
        try:
            parsed = datetime.fromisoformat(value)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=source_tz)
            timestamps.append(parsed.astimezone(LOCAL_TZ))
        except ValueError:
            continue
    return max(timestamps) if timestamps else None


def latest_source_time(
    *datasets: tuple[list[dict[str, str]], str, tzinfo]
) -> datetime | None:
    timestamps = [
        latest_datetime(rows, key, source_tz)
        for rows, key, source_tz in datasets
    ]
    found = [item for item in timestamps if item is not None]
    return max(found) if found else None


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


def metric_card(title: str, value: str, detail: str = "") -> str:
    detail_html = f"<div class='detail'>{html(detail)}</div>" if detail else ""
    return (
        "<section class='card'>"
        f"<h2>{html(title)}</h2>"
        f"<div class='value'>{html(value)}</div>"
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


def latest_rows() -> tuple[dict[str, str], dict[str, str], dict[str, str], datetime | None]:
    runtime = read_csv("runtime_snapshots.csv")
    energy = read_csv("energy_snapshots.csv")
    day = read_csv("day_multiline_samples.csv")
    latest_time = latest_source_time(
        (runtime, "server_time", timezone.utc),
        (energy, "server_time", timezone.utc),
        (day, "sample_time", LOCAL_TZ),
    )
    latest_runtime = runtime[-1] if runtime else {}
    latest_energy = energy[-1] if energy else {}
    latest_day = day[-1] if day else {}
    return latest_runtime, latest_energy, latest_day, latest_time


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
"""


def build_portal() -> str:
    now = datetime.now(LOCAL_TZ)
    runtime, energy, day, latest_time = latest_rows()

    status = field(runtime, "status_text")
    soc = as_float(runtime, "soc")
    day_time = latest_datetime([day], "sample_time", LOCAL_TZ) if day else None
    day_age_minutes = (
        (now - day_time).total_seconds() / 60 if day_time else None
    )
    day_is_fresh = (
        day_age_minutes is not None
        and 0 <= day_age_minutes <= DAY_TELEMETRY_MAX_AGE_MINUTES
    )
    ac_power = as_float(day, "ac_couple_power_w") if day_is_fresh else None
    load = as_float(day, "consumption_w") if day_is_fresh else None
    day_detail = (
        f"Sample: {day_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        if day_is_fresh
        else "Day telemetry stale or unavailable"
    )
    source_time = latest_time.strftime("%Y-%m-%d %H:%M:%S %Z") if latest_time else "n/a"

    if latest_time:
        age_hours = (now - latest_time).total_seconds() / 3600
        freshness = f"{age_hours:.1f} hours old"
    else:
        freshness = "n/a"

    findings = "".join(
        f"<li>{html(item)}</li>" for item in engineering_findings()
    )

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>EG4 Local Portal</title>
<style>{CSS}</style>
</head>
<body>
<main>
<header>
<h1>EG4 Local Portal</h1>
<p>Generated {html(now.isoformat(timespec="seconds"))}</p>
</header>
<div class="grid">
{metric_card("System Status", status, field(runtime, "fw_code"))}
{gauge_card("Battery SOC", soc, 100, "%")}
{gauge_card("AC-couple Power", ac_power, 5400, " W", day_detail)}
{gauge_card("Load", load, 12000, " W", day_detail)}
{metric_card("Latest Source Time", source_time, freshness)}
{metric_card("Today Usage", fmt_num(as_float(energy, "today_usage_kwh"), " kWh"))}
</div>
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
