from pydantic import BaseModel


class BatterGameStatsBase(BaseModel):
    player_id: int
    game_id: int

    at_bats: int = 0
    hits: int = 0
    doubles: int = 0
    triples: int = 0
    home_runs: int = 0
    rbis: int = 0
    runs_scored: int = 0
    walks: int = 0
    strikeouts: int = 0
    stolen_bases: int = 0
    caught_stealing: int = 0

class BatterGameStatsRead(BatterGameStatsBase):
    id: int 

    class Config:
        orm_mode = True