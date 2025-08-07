from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models import Team, Game

class TeamRecord(Base):
    __tablename__ = "team_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id")) 
    date: Mapped[date]
    played: Mapped[bool] = mapped_column(default=False)
    won: Mapped[bool | None] = mapped_column(nullable=False)
    opponent_team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), nullable=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), nullable=True)

    team: Mapped["Team"] = relationship(foreign_keys=[team_id], back_populates="daily_records")
    opponent_team: Mapped["Team"] = relationship(foreign_keys=[opponent_team_id])
    game: Mapped["Game"] = relationship(foreign_keys=[game_id])