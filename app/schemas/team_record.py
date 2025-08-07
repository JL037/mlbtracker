from pydantic import BaseModel
from typing import Optional
from datetime import date

class TeamRecordBase(BaseModel):
    team_id: int
    date: date
    played: bool
    won: Optional[bool] = None
    opponent_team_id: Optional[int] = None
    game_id: Optional[int] = None

class TeamRecordRead(TeamRecordBase):
    id: int

    class Config:
        orm_mode = True