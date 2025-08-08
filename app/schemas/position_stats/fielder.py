from pydantic import BaseModel
from typing import Optional

class FielderGameStatsBase(BaseModel):
    player_id: int
    game_id: int

    position: Optional[str] = None
    putouts: int = 0 
    assists: int = 0
    errors: int = 0
    double_plays_turned: int = 0
    fielding_chance: int = 0 

class FielderGameStatsRead(FielderGameStatsBase):
    id: int

    class Config:
        orm_mode = True