import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import mean

REPORTS_DIR = Path("reports")
OUTPUT_FILE = REPORTS_DIR / "engineering_daily_report.md"

CSV_FILES = [
    "runtime_snapshots.csv",
    "energy_snapshots.csv",
    "day_multiline_samples.csv",
    "ac_couple_daily_samples.csv",
    "month_energy_days.csv",
    "set_records.csv",
]


def read_csv(filename: str) -> list[dict[str, str]]:
    path = REPORTS_DIR / filename
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def as_float(row: dict[str, str], key: str) -> float | None:
    value = (row.get(key) or "").strip()
    if value == "":
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


RAW_JSON_FIELD_MAP = {
    "param_name": "paramNameText",
    "value_text": "paramValue",
    "result_text": "success",
    "username": "actionUsername",
    "client_type": "clientType",
}


def field(row: dict[str, str], key: str) -> str:
    value = (row.get(key) or "").strip()
    if value:
        return value

    raw_key = RAW_JSON_FIELD_MAP.get(key)
    raw_json = row.get("raw_json") or ""

    if raw_key and raw_json:
        try:
            data = json.loads(raw_json)
        except json.JSONDecodeError:
            return "n/a"

        raw_value = data.get(raw_key)
        if raw_value is not None:
            return str(raw_value)

    return "n/a"


def values(rows: list[dict[str, str]], key: str) -> list[float]:
    result: list[float] = []
    for row in rows:
        value = as_float(row, key)
        if value is not None:
            result.append(value)
    return result


def summarize_range(rows: list[dict[str, str]], key: str) -> str:
    items = [field(row, key) for row in rows if field(row, key) != "n/a"]
    if not items:
        return "n/a"
    return f"{items[0]} to {items[-1]}"



def month_energy_kwh(row: dict[str, str], key: str) -> float | None:
    value = as_float(row, key)
    if value is None:
        return None
    return value / 10

def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def build_report() -> str:
    now = datetime.now().isoformat(timespec="seconds")

    runtime = read_csv("runtime_snapshots.csv")
    energy = read_csv("energy_snapshots.csv")
    day = read_csv("day_multiline_samples.csv")
    ac = read_csv("ac_couple_daily_samples.csv")
    month = read_csv("month_energy_days.csv")
    records = read_csv("set_records.csv")

    lines: list[str] = [
        "# EG4 Engineering Daily Report",
        "",
        f"Generated: {now}",
        "",
        "## Source Files",
        "",
    ]

    source_rows = []
    for filename in CSV_FILES:
        rows = read_csv(filename)
        status = "present" if (REPORTS_DIR / filename).exists() else "missing"
        source_rows.append([filename, status, str(len(rows))])
    lines.extend(markdown_table(["File", "Status", "Rows"], source_rows))

    lines.extend(["", "## Latest Runtime Snapshot", ""])

    if runtime:
        latest = runtime[-1]
        runtime_rows = [
            ["Serial", field(latest, "serial_num")],
            ["Server time", field(latest, "server_time")],
            ["Device time", field(latest, "device_time")],
            ["Firmware", field(latest, "fw_code")],
            ["Status", field(latest, "status_text")],
            ["SOC", fmt_num(as_float(latest, "soc"), "%")],
            ["Battery voltage", fmt_num(as_float(latest, "v_bat"), " V")],
            ["Grid frequency", fmt_num(as_float(latest, "grid_freq_hz"), " Hz")],
            ["EPS frequency", fmt_num(as_float(latest, "eps_freq_hz"), " Hz")],
            ["Consumption", fmt_num(as_float(latest, "consumption_power_w"), " W")],
            ["AC-couple power", fmt_num(as_float(latest, "ac_couple_power_w"), " W")],
            ["Radiator 1", fmt_num(as_float(latest, "radiator1_c"), " C")],
            ["Radiator 2", fmt_num(as_float(latest, "radiator2_c"), " C")],
        ]
        lines.extend(markdown_table(["Metric", "Value"], runtime_rows))
    else:
        lines.append("No runtime snapshots found.")

    lines.extend(["", "## Latest Energy Snapshot", ""])

    if energy:
        latest = energy[-1]
        energy_rows = [
            ["Server time", field(latest, "server_time")],
            ["Today usage", fmt_num(as_float(latest, "today_usage_kwh"), " kWh")],
            ["Today import", fmt_num(as_float(latest, "today_import_kwh"), " kWh")],
            ["Today charging", fmt_num(as_float(latest, "today_charging_kwh"), " kWh")],
            ["Today discharging", fmt_num(as_float(latest, "today_discharging_kwh"), " kWh")],
            ["Today export", fmt_num(as_float(latest, "today_export_kwh"), " kWh")],
            ["Total usage", fmt_num(as_float(latest, "total_usage_kwh"), " kWh")],
            ["Total import", fmt_num(as_float(latest, "total_import_kwh"), " kWh")],
            ["Total charging", fmt_num(as_float(latest, "total_charging_kwh"), " kWh")],
            ["Total discharging", fmt_num(as_float(latest, "total_discharging_kwh"), " kWh")],
        ]
        lines.extend(markdown_table(["Metric", "Value"], energy_rows))
    else:
        lines.append("No energy snapshots found.")

    lines.extend(["", "## Day Telemetry Summary", ""])

    if day:
        ac_values = values(day, "ac_couple_power_w")
        pv_values = values(day, "solar_pv_w")
        load_values = values(day, "consumption_w")
        soc_values = values(day, "soc")
        grid_values = values(day, "grid_power_w")
        battery_values = values(day, "battery_discharging_w")

        active_ac = [v for v in ac_values if v > 50]
        low_ac = [v for v in ac_values if v <= 50]
        active_pct = (len(active_ac) / len(ac_values) * 100) if ac_values else None
        low_pct = (len(low_ac) / len(ac_values) * 100) if ac_values else None
        ac_transitions = sum(1 for a, b in zip(ac_values, ac_values[1:]) if (a > 50) != (b > 50))

        day_rows = [
            ["Sample range", summarize_range(day, "sample_time")],
            ["Samples", str(len(day))],
            ["AC-couple active samples", str(len(active_ac))],
            ["AC-couple active percent", fmt_num(active_pct, "%")],
            ["AC-couple low/off samples", str(len(low_ac))],
            ["AC-couple low/off percent", fmt_num(low_pct, "%")],
            ["AC-couple active/off transitions", str(ac_transitions)],
            ["Max AC-couple power", fmt_num(max(ac_values) if ac_values else None, " W")],
            ["Average active AC-couple power", fmt_num(mean(active_ac) if active_ac else None, " W")],
            ["Max solar PV power", fmt_num(max(pv_values) if pv_values else None, " W")],
            ["Max consumption", fmt_num(max(load_values) if load_values else None, " W")],
            ["SOC range", f"{fmt_num(min(soc_values) if soc_values else None, '%')} to {fmt_num(max(soc_values) if soc_values else None, '%')}"],
            ["Grid power range", f"{fmt_num(min(grid_values) if grid_values else None, ' W')} to {fmt_num(max(grid_values) if grid_values else None, ' W')}"],
            ["Battery discharge range", f"{fmt_num(min(battery_values) if battery_values else None, ' W')} to {fmt_num(max(battery_values) if battery_values else None, ' W')}"],
        ]
        lines.extend(markdown_table(["Metric", "Value"], day_rows))
    else:
        lines.append("No day telemetry samples found.")

    lines.extend(["", "## Month Energy Summary", ""])

    if month:
        energy_fields = [
            "e_ac_couple_day",
            "e_load_day",
            "e_consumption_day",
            "e_pv1_day",
            "e_pv2_day",
            "e_chg_day",
            "e_dischg_day",
        ]

        nonzero_days = [
            row for row in month
            if any((as_float(row, key) or 0) != 0 for key in energy_fields)
        ]

        latest_day = nonzero_days[-1] if nonzero_days else month[-1]

        month_rows = [
            ["Month", field(latest_day, "month_text")],
            ["Days reported", str(len(month))],
            ["Latest day", field(latest_day, "day")],
            ["Latest AC-couple energy", fmt_num(month_energy_kwh(latest_day, "e_ac_couple_day"), " kWh")],
            ["Latest load energy", fmt_num(month_energy_kwh(latest_day, "e_load_day"), " kWh")],
            ["Latest consumption energy", fmt_num(month_energy_kwh(latest_day, "e_consumption_day"), " kWh")],
            ["Latest PV1 energy", fmt_num(month_energy_kwh(latest_day, "e_pv1_day"), " kWh")],
            ["Latest PV2 energy", fmt_num(month_energy_kwh(latest_day, "e_pv2_day"), " kWh")],
            ["Latest battery charge", fmt_num(month_energy_kwh(latest_day, "e_chg_day"), " kWh")],
            ["Latest battery discharge", fmt_num(month_energy_kwh(latest_day, "e_dischg_day"), " kWh")],
        ]
        lines.extend(markdown_table(["Metric", "Value"], month_rows))
    else:
        lines.append("No monthly energy rows found.")

    lines.extend(["", "## Remote Setting Records", ""])

    if records:
        params = Counter(field(row, "param_name") for row in records)
        latest_records = records[-10:]

        record_rows = [
            ["Record range", summarize_range(records, "record_time")],
            ["Total records", str(len(records))],
            ["Unique parameters", str(len(params))],
        ]
        lines.extend(markdown_table(["Metric", "Value"], record_rows))

        lines.extend(["", "### Most Common Parameters", ""])
        lines.extend(markdown_table(
            ["Parameter", "Count"],
            [[name, str(count)] for name, count in params.most_common(10)],
        ))

        lines.extend(["", "### Latest Records", ""])
        lines.extend(markdown_table(
            ["Time", "Parameter", "Value", "Result", "User", "Client"],
            [
                [
                    field(row, "record_time"),
                    field(row, "param_name"),
                    field(row, "value_text"),
                    field(row, "result_text"),
                    field(row, "username"),
                    field(row, "client_type"),
                ]
                for row in latest_records
            ],
        ))
    else:
        lines.append("No remote setting records found.")

    lines.extend(["", "## Engineering Findings", ""])

    findings = []

    if day:
        ac_values = values(day, "ac_couple_power_w")
        pv_values = values(day, "solar_pv_w")
        active_ac = [value for value in ac_values if value > 50]
        low_ac = [value for value in ac_values if value <= 50]
        active_pct = (len(active_ac) / len(ac_values) * 100) if ac_values else None
        low_pct = (len(low_ac) / len(ac_values) * 100) if ac_values else None
        ac_transitions = sum(1 for a, b in zip(ac_values, ac_values[1:]) if (a > 50) != (b > 50))

        findings.append(
            f"- AC-couple activity appeared in {len(active_ac)} of {len(day)} day samples ({fmt_num(active_pct, '%')})."
        )

        if ac_values:
            findings.append(
                f"- Peak AC-couple power was {fmt_num(max(ac_values), ' W')}."
            )

        if active_ac and pv_values and max(pv_values) == 0:
            findings.append(
                "- AC-coupled production is present while parsed solar PV remains 0 W."
            )

        if low_ac:
            findings.append(
                f"- AC-couple low/off samples were present: {len(low_ac)} samples ({fmt_num(low_pct, '%')})."
            )

        findings.append(
            f"- AC-couple active/off transitions detected: {ac_transitions}."
        )
    else:
        findings.append("- No day telemetry samples were available.")

    if month:
        findings.append(
            f"- Latest month-energy day with real data was day {field(latest_day, 'day')}."
        )

    if records:
        latest_record = records[-1]
        findings.append(
            "- Latest remote setting change: "
            f"{field(latest_record, 'param_name')} = {field(latest_record, 'value_text')} "
            f"at {field(latest_record, 'record_time')}."
        )

    lines.extend(findings)

    lines.extend(
        [
            "",
            "## Engineering Notes",
            "",
            "- Generated from existing EG4 collector CSV output.",
            "- Collector behavior unchanged.",
            "- SQLite schema unchanged.",
            "- Generated artifacts under reports/ are not source code unless intentionally version-controlled.",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    report = build_report()
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
