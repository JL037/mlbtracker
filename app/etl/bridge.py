from __future__ import annotations
from typing import List, Tuple, Dict, Any
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Team, Season
from app.etl.transform import GameIn

# If your Team model uses a different column for the MLB id,
# change Team.mlb_id below to match (e.g., Team.team_id)
EXTERNAL_TEAM_ID_COL = Team.team_id  # <-- adjust if needed

def _build_lookup_maps(db: Session) -> tuple[Dict[int, int], Dict[int, int]]:
    """Return (season_map, team_map):
       season_map: year -> season.id
       team_map:   mlb_team_id -> team.id
    """
    season_map = dict(db.execute(select(Season.year, Season.id)))
    team_map   = dict(db.execute(select(EXTERNAL_TEAM_ID_COL, Team.id)))
    return season_map, team_map

def bind_games_fks(
    db: Session,
    games: List[GameIn],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Convert GameIn (season_year + MLB team ids) into dicts with internal FKs:
    season_id, home_team_id, away_team_id. Returns (good_rows, rejected_rows).
    """
    if not games:
        return [], []

    season_map, team_map = _build_lookup_maps(db)
    good: List[Dict[str, Any]] = []
    bad:  List[Dict[str, Any]] = []

    for gi in games:
        sid = season_map.get(gi.season_year)
        ht  = team_map.get(gi.home_team_mlb_id)
        at  = team_map.get(gi.away_team_mlb_id)

        if not sid or not ht or not at:
            bad.append({
                "reason": "missing_fk",
                "game_id": gi.game_id,
                "season_year": gi.season_year,
                "home_team_mlb_id": gi.home_team_mlb_id,
                "away_team_mlb_id": gi.away_team_mlb_id,
            })
            continue

        good.append({
            "game_id": gi.game_id,
            "season_id": sid,
            "date": gi.date,
            "status": gi.status,
            "location": gi.location,
            "scheduled_start_time": gi.scheduled_start_time,
            "official_start_time": gi.official_start_time,
            "home_team_id": ht,
            "away_team_id": at,
        })

    return good, bad
