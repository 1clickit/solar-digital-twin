import argparse
import hashlib
from pathlib import Path
from datetime import datetime

from eg4_client import EG4PortalClient, save_json
from eg4_database import connect, upsert_runtime, upsert_energy, upsert_day_multiline, upsert_month_column, upsert_set_records
from eg4_reports import export_reports


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser(description="EG4 Portal Connector v4: login, download evidence, update SQLite, export CSV reports.")
    p.add_argument("--serial", required=True)
    p.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Date for dayMultiLine, YYYY-MM-DD")
    p.add_argument("--db", default=".\\eg4_digital_twin.sqlite")
    p.add_argument("--output-dir", default=".\\evidence")
    p.add_argument("--reports-dir", default=".\\reports")
    p.add_argument("--skip-set-records", action="store_true")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    captured_at = datetime.now().isoformat(timespec="seconds")
    evidence_dir = Path(args.output_dir) / run_id
    evidence_dir.mkdir(parents=True, exist_ok=True)

    print("Logging in to EG4 portal...")
    client = EG4PortalClient(verbose=args.verbose)
    login_info = client.login()
    save_json(login_info, evidence_dir / "login_metadata.json")

    conn = connect(args.db)
    conn.execute("INSERT OR REPLACE INTO sync_runs(run_id, started_at, serial_num, date_text, notes) VALUES (?,?,?,?,?)", (run_id, captured_at, args.serial, args.date, "eg4_sync v4"))

    saved = []
    def save_dataset(name, obj):
        path = save_json(obj, evidence_dir / f"{name}_{args.serial}_{run_id}.json")
        digest = sha256_file(path)
        conn.execute("INSERT INTO evidence_files(run_id,dataset,path,created_at,sha256) VALUES (?,?,?,?,?)", (run_id, name, str(path), captured_at, digest))
        saved.append(path)
        return path

    print("Downloading runtime...")
    runtime = client.get_runtime(args.serial)
    save_dataset("runtime", runtime)
    upsert_runtime(conn, args.serial, runtime, captured_at)

    print("Downloading energy info...")
    energy = client.get_energy_info(args.serial)
    save_dataset("energy_info", energy)
    upsert_energy(conn, args.serial, energy, captured_at, runtime.get("serverTime"))

    print(f"Downloading dayMultiLine for {args.date}...")
    day = client.get_day_multiline(args.serial, args.date)
    save_dataset("day_multiline", day)
    n_day = upsert_day_multiline(conn, args.serial, day)

    month_text = args.date[:7]
    print(f"Downloading monthColumn for {month_text}...")
    month = client.get_month_column(args.serial, month_text)
    save_dataset("month_column", month)
    n_month = upsert_month_column(conn, args.serial, month_text, month)

    n_set = 0
    if not args.skip_set_records:
        print("Downloading remote set records...")
        sets = client.get_set_records(args.serial)
        save_dataset("set_records", sets)
        n_set = upsert_set_records(conn, args.serial, sets)

    conn.commit()
    conn.close()

    print("Exporting CSV reports...")
    written = export_reports(args.db, args.reports_dir)

    print("\nSync complete.")
    print(f"Evidence folder: {evidence_dir}")
    print(f"SQLite DB: {args.db}")
    print(f"Inserted/updated day samples: {n_day}")
    print(f"Inserted/updated month rows: {n_month}")
    print(f"Inserted/updated set records: {n_set}")
    print("Reports:")
    for path, rows in written:
        print(f"  {path}" + (f" ({rows} rows)" if rows is not None else ""))

if __name__ == "__main__":
    main()
