from pydantic import BaseModel


class SeasonBase(BaseModel):
    year: int

class SeasonRead(SeasonBase):
    id: int

    class Config:
        orm_mode = True
