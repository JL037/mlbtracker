from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from datetime import date
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import Team, PitcherGameStats, BatterGameStats, FielderGameStats, PlayerTeamHistory

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    position: Mapped[str] = mapped_column(String, nullable=True)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), nullable=True)


    #Relationships
    team: Mapped["Team"] = relationship(back_populates="players")
    pitching_stats: Mapped[list["PitcherGameStats"]] = relationship(back_populates="player")
    batting_stats: Mapped[list["BatterGameStats"]] = relationship(back_populates="player")
    fielding_stats: Mapped[list["FielderGameStats"]] = relationship(back_populates="player")
    team_history: Mapped[list["PlayerTeamHistory"]] = relationship(back_populates="player")