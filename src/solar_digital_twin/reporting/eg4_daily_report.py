from datetime import datetime
from pathlib import Path

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


def count_data_rows(path: Path) -> int:
    if not path.exists():
        return 0

    lines = path.read_text(
        encoding="utf-8",
        errors="replace",
    ).splitlines()

    return max(len(lines) - 1, 0)


def build_report() -> str:
    now = datetime.now().isoformat(timespec="seconds")

    lines = [
        "# EG4 Engineering Daily Report",
        "",
        f"Generated: {now}",
        "",
        "## Source Files",
        "",
    ]

    for filename in CSV_FILES:
        path = REPORTS_DIR / filename
        status = "present" if path.exists() else "missing"
        rows = count_data_rows(path)

        lines.append(
            f"- `{filename}`: {status}, {rows} data rows"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Generated from the existing EG4 collector output.",
            "- Collector behavior unchanged.",
            "- SQLite schema unchanged.",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    REPORTS_DIR.mkdir(exist_ok=True)

    report = build_report()

    OUTPUT_FILE.write_text(
        report,
        encoding="utf-8",
    )

    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
