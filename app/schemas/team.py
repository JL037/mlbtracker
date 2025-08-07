from pydantic import BaseModel
from typing import Optional

class TeamBase(BaseModel):
    name: str
    location: Optional[str] = None
    league: Optional[str] = None
    division: Optional[str] = None

class TeamRead(TeamBase):
    id: int

    class Config:
        orm_mode = True