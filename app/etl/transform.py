from __future__ import annotations
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class TeamIn(BaseModel):
    team_id: int = Field(..., alias="id")
    name: str
    abbreviation: Optional[str] = None
    location: Optional[str] = None
    league: Optional[str] = None
    division: Optional[str] = None

def map_team(team: Dict[str, Any]) -> TeamIn:
    league = (team.get("league") or {}).get("name")
    division = (team.get("division") or {}).get("name")
    loc = team.get("locationName") or team.get("venue", {}).get("city")
    abbr = team.get("abbreviation")
    return TeamIn(
        id=team["id"],
        name=team["name"],
        abbreviation=abbr,
        location=loc,
        league=league,
        division=division,
    )


class SeasonIn(BaseModel):
    year: int


def build_seasons(start: int, end_inclusive: int) -> List[SeasonIn]:
    return [SeasonIn(year=y) for y in range(start, end_inclusive + 1)]
    

class GameIn(BaseModel):
    game_id: int
    date: str
    status: Optional[str] = None
    location: Optional[str] = None
    season_year: int
    scheduled_start_time: Optional[str] = None
    official_start_time: Optional[str] = None
    home_team_mlb_id: Optional[int] = None
    away_team_mlb_id: Optional[int] = None


def map_games_from_schedule(dates: List[Dict[str, Any]], year: int) -> List[GameIn]:
    rows: List[GameIn] = []
    for date in dates:
        for game in date.get("games", []):
            if game.get("gameType") != "R":
                continue
            teams = game.get("teams") or {}
            home = (teams.get("home") or {}).get("team") or {}
            away = (teams.get("away") or {}).get("team") or {}

            # if (home.get("sport") or {}).get("id") != 1 or (away.get("sport") or {}).get("id") != 1:
            #     continue
            
            rows.append(
                GameIn(
                    game_id=game["gamePk"],
                    date=game.get("officialDate") or game.get("gameDate"),
                    status=(game.get("status") or {}).get("detailedState"),
                    location=(game.get("venue") or {}).get("name"),
                    season_year=year,
                    scheduled_start_time=game.get("gameDate"),
                    official_start_time=(game.get("OfficialStartTime") or None),
                    home_team_mlb_id=home.get("id"),
                    away_team_mlb_id=away.get("id"),
                )
            )
    return rows

