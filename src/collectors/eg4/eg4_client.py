import os
import json
from pathlib import Path
from datetime import datetime
import requests

BASE_URL = "https://monitor.eg4electronics.com"

class EG4PortalClient:
    def __init__(self, username=None, password=None, base_url=BASE_URL, timeout=30, verbose=False):
        self.username = username or os.getenv("EG4_USERNAME")
        self.password = password or os.getenv("EG4_PASSWORD")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/WManage/web/login",
        })

    def login(self):
        if not self.username or not self.password:
            raise RuntimeError("Missing EG4_USERNAME or EG4_PASSWORD environment variable.")
        login_url = f"{self.base_url}/WManage/web/login"
        r0 = self.session.get(login_url, timeout=self.timeout)
        r = self.session.post(
            login_url,
            data={"account": self.username, "password": self.password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            allow_redirects=False,
            timeout=self.timeout,
        )
        location = r.headers.get("Location")
        if location:
            final_url = location if location.startswith("http") else f"{self.base_url}{location}"
            rf = self.session.get(final_url, timeout=self.timeout)
        else:
            rf = r
        ok = (r.status_code in (200, 302, 303)) and bool(self.session.cookies.get("JSESSIONID"))
        result = {
            "success": ok,
            "initial_login_page_status": r0.status_code,
            "login_post_status": r.status_code,
            "redirect_location": location,
            "jsessionid_present": bool(self.session.cookies.get("JSESSIONID")),
            "final_status_after_redirect": getattr(rf, "status_code", None),
            "final_url_after_redirect": getattr(rf, "url", None),
        }
        if self.verbose:
            print(json.dumps(result, indent=2))
        if not ok:
            raise RuntimeError(f"EG4 login failed: {result}")
        return result

    def _post_json(self, path, data, referer=None):
        url = f"{self.base_url}{path}"
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest"}
        if referer:
            headers["Referer"] = f"{self.base_url}{referer}"
        r = self.session.post(url, data=data, headers=headers, timeout=self.timeout)
        r.raise_for_status()
        try:
            return r.json()
        except Exception as e:
            raise RuntimeError(f"Endpoint did not return JSON: {path}; status={r.status_code}; first bytes={r.text[:200]!r}") from e

    def get_runtime(self, serial):
        return self._post_json("/WManage/api/inverter/getInverterRuntime", {"serialNum": serial}, "/WManage/web/monitor/inverter")

    def get_energy_info(self, serial):
        return self._post_json("/WManage/api/inverter/getInverterEnergyInfo", {"serialNum": serial}, "/WManage/web/monitor/inverter")

    def get_day_multiline(self, serial, date_text):
        return self._post_json("/WManage/api/analyze/chart/dayMultiLine", {"serialNum": serial, "dateText": date_text}, "/WManage/web/analyze/chart")

    def get_month_column(self, serial, date_text):
        # Browser HAR showed this endpoint expects separate year/month fields,
        # not dateText. date_text may be YYYY-MM or YYYY-MM-DD.
        year = str(date_text)[:4]
        month = str(int(str(date_text)[5:7]))
        return self._post_json(
            "/WManage/api/inverterChart/monthColumn",
            {"serialNum": serial, "year": year, "month": month},
            "/WManage/web/monitor/inverter",
        )

    def get_set_records(self, serial, page=1, rows=2000, show_auto=False):
        return self._post_json("/WManage/web/maintain/remoteSetRecord/list", {
            "page": page,
            "rows": rows,
            "serialNum": serial,
            "showAutoSetRecord": str(show_auto).lower(),
        }, "/WManage/web/maintain/remoteSetRecord")


def save_json(obj, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
