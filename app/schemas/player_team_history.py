from pydantic import BaseModel
from datetime import date
from typing import Optional

class PlayerTeamHistoryBase(BaseModel):
    player_id: int
    team_id: int
    start_date: date
    end_date: Optional[date] = None

class PlayerTeamHistoryRead(PlayerTeamHistoryBase):
    id: int

    class Config:
        orm_mode = True