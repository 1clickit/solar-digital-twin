from pathlib import Path

REPORTS_DIR = Path("reports")

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

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return max(len(lines) - 1, 0)


def main() -> None:
    print("EG4 Daily Report")
    print()

    for filename in CSV_FILES:
        path = REPORTS_DIR / filename
        status = "present" if path.exists() else "missing"
        rows = count_data_rows(path)
        print(f"{filename}: {status}, {rows} data rows")


if __name__ == "__main__":
    main()
