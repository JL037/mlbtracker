from __future__ import annotations
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert

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
        insert_stmt = pg_insert(Team).values(dicts)
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
        insert_stmt = pg_insert(Season).values(dicts)
        upsert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=[Season.year])
        sesh.execute(upsert_stmt)
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

CHUNK_SIZE = 500

_STATUS_RANK = {"Final": 4, "Game Over": 4, "In Progress": 3, "Delayed": 2, "Pre-Game": 1}

def _pick_better(a: dict, b: dict) -> dict:
    # Higher status rank wins
    ra = _STATUS_RANK.get((a.get("status") or ""), 0)
    rb = _STATUS_RANK.get((b.get("status") or ""), 0)
    if ra != rb:
        return a if ra > rb else b
    # Prefer presence of official_start_time
    if bool(a.get("official_start_time")) != bool(b.get("official_start_time")):
        return a if a.get("official_start_time") else b
    # Prefer later scheduled_start_time
    sa = a.get("scheduled_start_time") or ""
    sb = b.get("scheduled_start_time") or ""
    return a if sa >= sb else b

def _dedupe_by_game_id(rows: list[dict]) -> list[dict]:
    by_id: dict[int, dict] = {}
    for d in rows:
        gid = d["game_id"]
        if gid in by_id:
            by_id[gid] = _pick_better(by_id[gid], d)
        else:
            by_id[gid] = d
    return list(by_id.values())

def upsert_games(rows: List[GameIn]) -> int:
    if not rows:
        return 0

    dicts = []
    skipped = 0
    with get_session() as sesh:
        season_cache: dict[int, int] = {}
        def season_id_for(y: int) -> int:
            if y not in season_cache:
                season_cache[y] = _season_id_by_year(sesh, y)
            return season_cache[y]

        for row in rows:
            if not (row.home_team_mlb_id and row.away_team_mlb_id):
                skipped += 1
                continue
            home_pk = _team_id_by_team_id(sesh, row.home_team_mlb_id)
            away_pk = _team_id_by_team_id(sesh, row.away_team_mlb_id)
            if home_pk is None or away_pk is None:
                skipped += 1
                continue

            dicts.append({
                "game_id": row.game_id,
                "date": row.date,
                "status": row.status,
                "location": row.location,
                "season_id": season_id_for(row.season_year),
                "scheduled_start_time": row.scheduled_start_time,
                "official_start_time": row.official_start_time,
                "home_team_id": home_pk,
                "away_team_id": away_pk,
            })

        if not dicts:
            if skipped:
                print(f"Skipped {skipped} rows with missing team ids.")
            return 0

       
        original_len = len(dicts)
        dicts = _dedupe_by_game_id(dicts)
        removed = original_len - len(dicts)
        if removed:
            print(f"Removed {removed} duplicate game_ids before upsert.")

        total = 0
        for i in range(0, len(dicts), CHUNK_SIZE):
            chunk = dicts[i:i + CHUNK_SIZE]
            insert_stmt = pg_insert(Game).values(chunk)
            upsert_stmt = insert_stmt.on_conflict_do_update(
                index_elements=[Game.game_id],
                set_={
                    "date": insert_stmt.excluded.date,
                    "status": insert_stmt.excluded.status,
                    "location": insert_stmt.excluded.location,
                    "season_id": insert_stmt.excluded.season_id,
                    "scheduled_start_time": insert_stmt.excluded.scheduled_start_time,
                    "official_start_time": insert_stmt.excluded.official_start_time,
                    "home_team_id": insert_stmt.excluded.home_team_id,
                    "away_team_id": insert_stmt.excluded.away_team_id,
                }
            )
            sesh.execute(upsert_stmt)
            sesh.commit()
            total += len(chunk)

        if skipped:
            print(f"Skipped {skipped} rows with missing team ids.")
        return total
