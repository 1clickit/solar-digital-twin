import sqlite3
import json
from pathlib import Path
from datetime import datetime

SCHEMA = """
CREATE TABLE IF NOT EXISTS sync_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT UNIQUE NOT NULL,
    started_at TEXT NOT NULL,
    serial_num TEXT NOT NULL,
    date_text TEXT,
    notes TEXT
);
CREATE TABLE IF NOT EXISTS evidence_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    dataset TEXT NOT NULL,
    path TEXT NOT NULL,
    created_at TEXT NOT NULL,
    sha256 TEXT
);
CREATE TABLE IF NOT EXISTS runtime_snapshots (
    serial_num TEXT NOT NULL,
    server_time TEXT,
    device_time TEXT,
    fw_code TEXT,
    status_text TEXT,
    soc REAL,
    v_bat REAL,
    grid_freq_hz REAL,
    eps_freq_hz REAL,
    consumption_power_w REAL,
    ac_couple_power_w REAL,
    radiator1_c REAL,
    radiator2_c REAL,
    raw_json TEXT NOT NULL,
    captured_at TEXT NOT NULL,
    PRIMARY KEY(serial_num, captured_at)
);
CREATE TABLE IF NOT EXISTS energy_snapshots (
    serial_num TEXT NOT NULL,
    server_time TEXT,
    today_usage_kwh REAL,
    today_import_kwh REAL,
    today_charging_kwh REAL,
    today_discharging_kwh REAL,
    today_export_kwh REAL,
    total_usage_kwh REAL,
    total_import_kwh REAL,
    total_charging_kwh REAL,
    total_discharging_kwh REAL,
    raw_json TEXT NOT NULL,
    captured_at TEXT NOT NULL,
    PRIMARY KEY(serial_num, captured_at)
);
CREATE TABLE IF NOT EXISTS day_multiline_samples (
    serial_num TEXT NOT NULL,
    sample_time TEXT NOT NULL,
    solar_pv_w REAL,
    grid_power_w REAL,
    battery_discharging_w REAL,
    consumption_w REAL,
    soc REAL,
    ac_couple_power_w REAL,
    raw_json TEXT NOT NULL,
    PRIMARY KEY(serial_num, sample_time)
);
CREATE TABLE IF NOT EXISTS month_energy_days (
    serial_num TEXT NOT NULL,
    month_text TEXT NOT NULL,
    day INTEGER NOT NULL,
    e_pv1_day REAL,
    e_pv2_day REAL,
    e_pv3_day REAL,
    e_inv_day REAL,
    e_rec_day REAL,
    e_chg_day REAL,
    e_dischg_day REAL,
    e_eps_day REAL,
    e_to_grid_day REAL,
    e_to_user_day REAL,
    e_gen_day REAL,
    e_ac_couple_day REAL,
    e_load_day REAL,
    e_consumption_day REAL,
    raw_json TEXT NOT NULL,
    PRIMARY KEY(serial_num, month_text, day)
);
CREATE TABLE IF NOT EXISTS set_records (
    serial_num TEXT NOT NULL,
    record_id TEXT NOT NULL,
    record_time TEXT,
    param_name TEXT,
    value_text TEXT,
    result_text TEXT,
    username TEXT,
    client_type TEXT,
    raw_json TEXT NOT NULL,
    PRIMARY KEY(serial_num, record_id)
);
"""

def connect(db_path):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True) if Path(db_path).parent != Path('.') else None
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(SCHEMA)
    return conn

def j(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)

def n10(v):
    # EG4 often stores energy as tenths of kWh in raw numeric fields.
    try:
        return float(v) / 10.0
    except Exception:
        return None

def upsert_runtime(conn, serial, data, captured_at):
    conn.execute("""
    INSERT OR REPLACE INTO runtime_snapshots VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        serial, data.get("serverTime"), data.get("deviceTime"), data.get("fwCode"), data.get("statusText"),
        data.get("soc"), (data.get("vBat")/10 if isinstance(data.get("vBat"),(int,float)) else data.get("vBat")),
        (data.get("fac")/100 if isinstance(data.get("fac"),(int,float)) else data.get("fac")),
        (data.get("feps")/100 if isinstance(data.get("feps"),(int,float)) else data.get("feps")),
        data.get("consumptionPower"), data.get("acCouplePower"), data.get("tradiator1"), data.get("tradiator2"),
        j(data), captured_at
    ))

def upsert_energy(conn, serial, data, captured_at, server_time=None):
    conn.execute("""
    INSERT OR REPLACE INTO energy_snapshots VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        serial, server_time,
        n10(data.get("todayUsage")), n10(data.get("todayImport")), n10(data.get("todayCharging")),
        n10(data.get("todayDischarging")), n10(data.get("todayExport")), n10(data.get("totalUsage")),
        n10(data.get("totalImport")), n10(data.get("totalCharging")), n10(data.get("totalDischarging")),
        j(data), captured_at
    ))

def upsert_day_multiline(conn, serial, data):
    count = 0
    for r in data.get("data", []) or []:
        t = r.get("time")
        if not t:
            continue
        conn.execute("""
        INSERT OR REPLACE INTO day_multiline_samples VALUES (?,?,?,?,?,?,?,?,?)
        """, (serial, t, r.get("solarPv"), r.get("gridPower"), r.get("batteryDischarging"), r.get("consumption"), r.get("soc"), r.get("acCouplePower"), j(r)))
        count += 1
    return count

def upsert_month_column(conn, serial, month_text, data):
    count = 0
    for r in data.get("data", []) or []:
        day = r.get("day")
        if day is None:
            continue
        conn.execute("""
        INSERT OR REPLACE INTO month_energy_days VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (serial, month_text, day, r.get("ePv1Day"), r.get("ePv2Day"), r.get("ePv3Day"), r.get("eInvDay"), r.get("eRecDay"), r.get("eChgDay"), r.get("eDisChgDay"), r.get("eEpsDay"), r.get("eToGridDay"), r.get("eToUserDay"), r.get("eGenDay"), r.get("eAcCoupleDay"), r.get("eLoadDay"), r.get("eConsumptionDay"), j(r)))
        count += 1
    return count

def _record_id(r, idx):
    for k in ("id", "recordId", "uuid"):
        if k in r and r[k] not in (None, ""):
            return str(r[k])
    return f"row_{idx}_{r.get('createTime') or r.get('time') or ''}_{r.get('paramName') or r.get('name') or ''}"

def upsert_set_records(conn, serial, data):
    rows = data.get("rows", []) or []
    count = 0
    for idx, r in enumerate(rows):
        rid = _record_id(r, idx)
        keys = {k.lower(): k for k in r.keys()}
        def pick(*names):
            for name in names:
                if name.lower() in keys:
                    return r.get(keys[name.lower()])
            return None
        conn.execute("""
        INSERT OR REPLACE INTO set_records VALUES (?,?,?,?,?,?,?,?,?)
        """, (serial, rid, pick("createTime","time","dateTime"), pick("paramName","setName","name"), pick("value","setValue","paramValue"), pick("result","success","status","resultText"), pick("userName","account","operator"), pick("clientType","source"), j(r)))
        count += 1
    return count
