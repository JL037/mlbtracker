from __future__ import annotations
import argparse
import datetime as dt
from typing import List

from app.etl.fetch_data import get_schedule_for_season, get_teams
from app.etl.transform import map_games_from_schedule, map_team, build_seasons
from app.etl.load import upsert_games, upsert_seasons, upsert_teams

def cmd_bootstrap(args):
    print("-> Fetching teams..")
    teams_raw = get_teams(active_only=True)
    teams = [map_team(team) for team in teams_raw]
    summary_team = upsert_teams(teams)
    print(f"Upserted {summary_team} teams")

    current_year = dt.date.today().year
    print(f"Inserting seasons...{current_year}")
    seasons = build_seasons(2016, current_year)
    summary_season = upsert_seasons(seasons)
    print(f"Upserted {summary_season} seasons (idempotent)")

def cmd_season(args):
    year = int(args.year)
    print(f"-> Loading season {year} schedule..")
    dates = get_schedule_for_season(year)
    total_games = sum(len(d.get("games", [])) for d in dates)
    print(f"Fetched {len(dates)} days, {total_games} games from API")
    games = map_games_from_schedule(dates, year)
    print(f"Mapped {len(games)} games to GameIn rows")
    result = upsert_games(games)
    print(f"Upserted {result} games for {year}")
    total_games = sum(len(d.get("games", [])) for d in dates)
    print(f"Fetched {len(dates)} days, {total_games} games")


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

    
     