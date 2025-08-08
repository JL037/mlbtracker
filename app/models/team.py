from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import Player, Game, PlayerTeamHistory

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str]
    abbreviation: Mapped[str | None] = mapped_column(nullable=True)
    location: Mapped[str | None] = mapped_column(nullable=True)
    league: Mapped[str | None] = mapped_column(nullable=True)
    division: Mapped[str | None] = mapped_column(nullable=True)
    

    #Relationships
    home_games: Mapped[list["Game"]] = relationship(
        back_populates="home_team",
        foreign_keys="Game.home_team_id"
    )
    away_games: Mapped[list["Game"]] = relationship(
        back_populates="away_team",
        foreign_keys="Game.away_team_id"
    )

    players: Mapped[list["Player"]] = relationship(
        back_populates="team",
        cascade="all, delete-orphan"
    )
    player_history: Mapped[list["PlayerTeamHistory"]] = relationship(back_populates="team")