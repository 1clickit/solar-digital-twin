#!/usr/bin/env bash
set -euo pipefail

DATE_TEXT="${1:-$(date +%F)}"

python src/solar_digital_twin/collectors/eg4/eg4_sync.py --date "$DATE_TEXT"
python src/solar_digital_twin/reporting/eg4_daily_report.py
python -m solar_digital_twin.reporting.eg4_portal
