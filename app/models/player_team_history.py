from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from datetime import date
from app.models import Player, Team

class PlayerTeamHistory(Base):
    __tablename__ = "player_team_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)

    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date | None] = mapped_column(nullable=True)


    #Relationships
    player: Mapped["Player"] = relationship(back_populates="team_history")
    team: Mapped["Team"] = relationship(back_populates="player_history")