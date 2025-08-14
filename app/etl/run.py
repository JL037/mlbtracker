from __future__ import annotations
import argparse
import datetime as dt
from typing import List

from app.db.session import SessionLocal
from app.etl import fetch_data, transform
from app.etl.bridge import bind_games_fks
from app.etl.fetch_data import get_schedule_for_season, get_teams
from app.etl.transform import map_games_from_schedule, map_team, build_seasons
from app.etl.load import upsert_games, upsert_seasons, upsert_teams

def cmd_bootstrap(args):
        print("-> Fetching teams...")
        teams_raw = get_teams(active_only=True)
        teams = [map_team(t) for t in teams_raw]
        if len(teams) < 30:
            raise RuntimeError(f"Expected at least 30 MLB teams, got {len(teams)}")
        upserted_teams = upsert_teams(teams)
        print(f"Upserted {upserted_teams} teams")

        current_year = dt.date.today().year
        print(f"-> Inserting seasons 2016-{current_year}..")
        seasons = build_seasons(2016, current_year)
        expected = current_year - 2016 + 1
        if len (seasons) != expected:
            print(f"Warning: built {len(seasons)} seasons, expected {expected}")
        upserted_seasons = upsert_seasons(seasons)
        print(f"Upserted {upserted_seasons} seasons (idempotent)")

def cmd_season(args):
    year = args.year
        # 1) EXTRACT
    schedule = fetch_data.fetch_season_schedule(year)  # list of date buckets

        # nice-to-have stats
    total_days = len(schedule)
    total_games = sum(len(d.get("games", [])) for d in schedule)
    print(f"Fetched {total_days} days, {total_games} games from API")

        # 2) TRANSFORM (API → typed rows with external ids)
    game_ins = transform.map_games_from_schedule(schedule, year)
    print(f"Mapped {len(game_ins)} games to GameIn rows")

        # 3) BRIDGE (bind external ids → internal FK ids)
    bound_rows, rejected = bind_games_fks(game_ins)
    if rejected:
        print(
            f"Skipped {len(rejected)} games due to missing season/team ids "
            "(run `bootstrap` first to upsert teams/seasons)."
        )

    # 4) LOAD (ready-to-insert rows)
    upserted = upsert_games(bound_rows)
    print(f"Upserted {upserted} games for {year}.")


def cmd_daily(args):
    today = dt.date.today()
    yesterday = today - dt.timedelta(days=1)
    tomorrow = today + dt.timedelta(days=1)
    year = today.year
    print(f"(Daily) refreshing games for {year} (basic mode)..")

def main():
     argpars = argparse.ArgumentParser("MLB ETL runner")
     subcmd = argpars.add_subparsers(dest="cmd", required=True)
     boot = subcmd.add_parser("bootstrap", help="Upsert teams + seasons")
     boot.set_defaults(func=cmd_bootstrap)

     season_sub = subcmd.add_parser("season", help="Load/refresh games for a season")
     season_sub.add_argument("year", type=int)
     season_sub.set_defaults(func=cmd_season)

     daily_sub = subcmd.add_parser("daily", help="Basic daily refresh (placeholder)")
     daily_sub.set_defaults(func=cmd_daily)

     args = argpars.parse_args()
     args.func(args)

if __name__ == "__main__":
    main()

    
     