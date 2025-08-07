from pydantic import BaseModel
from datetime import date
from typing import Optional

class PlayerBase(BaseModel):
    id: int
    name: str
    birth_date: Optional[date] = None
    position: Optional[str] = None
    team_id: Optional[int] = None


class PlayerRead(PlayerBase):
    pass 


    class Config:
        orm_mode = True