from __future__ import annotations
import os, time, json
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.error

API_BASE = os.getenv("MLB_API_BASE", "https://statsapi.mlb.com/api/v1")
DEBUG_RAW = os.getenv("DEBUG_RAW", "0") == "1"

def _get(url: str) -> Dict[str, Any]:
    # basic retry/backoff for 429/5xx
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                data = resp.read().decode("utf-8")
                return json.loads(data)
        except urllib.error.HTTPError as e:
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

def get_schedule_for_season(year: int) -> List[Dict[str, Any]]:
    url = f"{API_BASE}/schedule/?sportsId=1&season={year}"
    payload = _get(url)
    dates = payload.get("dates", [])
    if DEBUG_RAW:
        os.makedirs(f"/tmp/mlb_raw/{year}", exist_ok=True)
        with open(f"/tmp/mlb_raw/{year}/schedule.json", "w") as f:
            json.dump(payload, f, indent=2)
    return dates

