import csv
import sqlite3
from pathlib import Path

QUERIES = {
    "runtime_snapshots.csv": "SELECT * FROM runtime_snapshots ORDER BY captured_at",
    "energy_snapshots.csv": "SELECT * FROM energy_snapshots ORDER BY captured_at",
    "day_multiline_samples.csv": "SELECT * FROM day_multiline_samples ORDER BY sample_time",
    "month_energy_days.csv": "SELECT * FROM month_energy_days ORDER BY month_text, day",
    "set_records.csv": "SELECT * FROM set_records ORDER BY record_time",
    "ac_couple_daily_samples.csv": "SELECT sample_time, ac_couple_power_w, soc, consumption_w, battery_discharging_w FROM day_multiline_samples WHERE ac_couple_power_w IS NOT NULL ORDER BY sample_time",
}

def export_reports(db_path, reports_dir):
    reports_dir = Path(reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    written = []
    for fname, query in QUERIES.items():
        cur = conn.execute(query)
        path = reports_dir / fname
        with path.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow([d[0] for d in cur.description])
            rows = cur.fetchall()
            w.writerows(rows)
        written.append((str(path), len(rows)))
    summary = reports_dir / "analysis_summary.txt"
    counts = {}
    for table in ["runtime_snapshots","energy_snapshots","day_multiline_samples","month_energy_days","set_records"]:
        counts[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    ac = conn.execute("SELECT MIN(sample_time), MAX(sample_time), MAX(ac_couple_power_w), AVG(ac_couple_power_w) FROM day_multiline_samples WHERE ac_couple_power_w > 0").fetchone()
    summary.write_text(
        "EG4 Portal Connector v4 Summary\n"
        "================================\n"
        + "\n".join(f"{k}: {v}" for k,v in counts.items())
        + f"\n\nAC-couple active window: {ac[0]} to {ac[1]}\nAC-couple max W: {ac[2]}\nAC-couple average W while active: {ac[3]}\n",
        encoding="utf-8"
    )
    written.append((str(summary), None))
    conn.close()
    return written
