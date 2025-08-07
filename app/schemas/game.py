from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GameBase(BaseModel):
    game_id: str
    season_id: int
    date: datetime
    status: Optional[str] = None
    location: Optional[str] = None
    scheduled_start_time: Optional[datetime] = None
    official_start_time: Optional[datetime] = None
    game_duration: Optional[str] = None
    calculated_end_time: Optional[datetime] = None
    temperature: Optional[str] = None
    weather_condition: Optional[str] = None
    wind: Optional[str] = None
    home_team_id: int
    away_team_id: int

class GameRead(GameBase):
    id: int

    class Config:
        orm_mode = True