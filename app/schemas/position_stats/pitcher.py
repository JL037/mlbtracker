from pydantic import BaseModel

class PitcherGameStatsBase(BaseModel):
    player_id: int
    game_id: int

    innings_pitched: float = 0
    hits_allowed: int = 0
    earned_runs: int = 0
    strikeouts: int = 0
    walks: int = 0
    home_runs_allowed: int = 0

    pitches_thrown: int = 0
    balls_thrown: int = 0
    strikes_thrown: int = 0

class PitcherGameStatsRead(PitcherGameStatsBase):
    id: int

    class Config:
        orm_mode = True