from __future__ import annotations
import os, time, json
from typing import Any, Dict, List
import urllib.request
import urllib.error
from urllib.parse import urlencode
import datetime as dt

API_BASE = os.getenv("MLB_API_BASE", "https://statsapi.mlb.com/api/v1")
DEBUG_RAW = os.getenv("DEBUG_RAW", "0") == "1"

def _get(url: str) -> Dict[str, Any]:
    # basic retry/backoff for 429/5xx
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
            
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore") if e.fp else ""
            print(f"[HTTP {e.code}] {url}\n{body[:400]}")
            if e.code in (429, 500, 502, 503, 504) and attempt < 4:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise
        except urllib.error.URLError:
            if attempt < 4:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise

def get_teams(active_only: bool = True) -> List[Dict[str, Any]]:
    url = f"{API_BASE}/teams"
    if active_only:
        url += "?activeStatus=yes"
    payload = _get(url)
    teams = payload.get("teams", [])
    if DEBUG_RAW:
        os.makedirs("/tmp/mlb_raw", exist_ok=True)
        with open("/tmp/mlb_raw/teams.json", "w") as f:
            json.dump(payload, f, indent=2)
    return teams

def _fetch_schedule_range(start: str, end: str) -> List[Dict[str, Any]]:
    url = f"{API_BASE}/schedule?sportId=1&startDate={start}&endDate={end}&gameTypes=R"
    payload = _get(url)
    return payload.get("dates", [])


def get_schedule_for_season(year: int) -> List[Dict[str, Any]]:
    start = dt.date(year, 1, 1)
    end = dt.date(year, 12, 31)
    step = dt.timedelta(days=28)
    
    dates: List[Dict[str, Any]] = []
    cur = start
    while cur <= end:
        win_end = min(cur + step, end)
        dates.extend(_fetch_schedule_range(cur.isoformat(), win_end.isoformat()))
        cur = win_end + dt.timedelta(days=1)
    return dates

