from __future__ import annotations
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.db.session import SessionLocal
from app.models import Team, Game, Season
from app.etl.transform import TeamIn, GameIn, SeasonIn

def get_session() -> Session:
    return SessionLocal()

def upsert_teams(rows: List[TeamIn]) -> int:
    if not rows:
        return 0
    dicts = [row.model_dump(by_alias=False) for row in rows]
    with get_session() as sesh:
        insert_stmt = insert(Team).values(dicts)
        upsert_stmt = insert_stmt.on_conflict_do_update(index_elements=[Team.team_id], set_={
            "name": insert_stmt.excluded.name,
            "abbreviation": insert_stmt.excluded.abbreviation,
            "location": insert_stmt.excluded.location,
            "league": insert_stmt.excluded.league,
        },
    )
        res = sesh.execute(upsert_stmt)
        sesh.commit()

        return len(dicts)

def upsert_seasons(rows: List[SeasonIn]) -> int:
    if not rows:
        return 0
    dicts = [row.model_dump() for row in rows]
    with get_session() as sesh:
        insert_stmt = insert(Season).values(dicts)
        upsert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=[Season.year])
        sesh.execute(insert_stmt)
        sesh.commit()
        return len(dicts)
    
def _season_id_by_year(sesh: Session, year: int) -> int:
    season = sesh.scalar(select(Season).where(Season.year == year))
    if season is None:
        raise ValueError(f"Season {year} not found; insert it first.")
    return season.id

def _team_id_by_team_id(sesh: Session, mlb_team_id: int) -> int:
    # helper for team FK lookups later
    team = sesh.scalar(select(Team).where(Team.team_id == mlb_team_id))
    if team is None:
        raise ValueError(f"Team with team_id={mlb_team_id} not found")
    return team.id

def upsert_games(rows: List[GameIn]) -> int:
    if not rows:
        return 0
    dicts = []
    with get_session as sesh:
        for row in rows:
            season_id = _season_id_by_year(sesh, row.season_year)
            dicts.append({
                "game_id": row.game_id,
                "date": row.date,
                "status": row.status,
                "location": row.location,
                "season_id": season_id,
                "scheduled_start_time": row.scheduled_start_time,
                "official_start_time": row.official_start_time,
            })
            insert_stmt = insert(Game).values(dicts)
            upsert_stmt = insert_stmt.on_conflict_do_update(
                index_elements=[Game.game_id],
                set_={
                    "date": insert_stmt.excluded.date,
                    "status": insert_stmt.excluded.status,
                    "location": insert_stmt.excluded.location,
                    "season_id": insert_stmt.excluded.season_id,
                    "scheduled_start_time": insert_stmt.excluded.scheduled_start_time,
                    "official_start_time": insert_stmt.excluded.official_start_time,
                }
            )
            sesh.execute(upsert_stmt)
            sesh.commit()
            return len(dicts)
        
    
        
