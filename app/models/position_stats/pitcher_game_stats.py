from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.models.base import Base
from app.models import Player, Game

class PitcherGameStats(Base):
    __tablename__ = "pitcher_game_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), nullable=False)

    innings_pitched: Mapped[float] = mapped_column(nullable=False)
    hits_allowed: Mapped[int] = mapped_column(default=0)
    earned_runs: Mapped[int] = mapped_column(default=0)
    strikeouts: Mapped[int] = mapped_column(default=0)
    walks: Mapped[int] = mapped_column(default=0)
    home_runs_allowed: Mapped[int] = mapped_column(default=0)
    pitches_thrown: Mapped[int] = mapped_column(default=0)
    balls_thrown: Mapped[int] = mapped_column(default=0)
    strikes_thrown: Mapped[int] = mapped_column(default=0)


    #Relationships
    player: Mapped["Player"] = relationship(back_populates="pitching_stats")
    game: Mapped["Game"] = relationship(back_populates="pitcher_stats")
