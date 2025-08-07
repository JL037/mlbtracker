from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models import Player, Game

class BatterGameStats(Base):
    __tablename__ = "batter_game_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), nullable=False)
 
    at_bats: Mapped[int] = mapped_column(default=0)
    hits: Mapped[int] = mapped_column(default=0)
    doubles: Mapped[int] = mapped_column(default=0)
    triples: Mapped[int] = mapped_column(default=0)
    home_runs: Mapped[int] = mapped_column(default=0)
    rbis: Mapped[int] = mapped_column(default=0)
    runs_scored: Mapped[int] = mapped_column(default=0)
    walks: Mapped[int] = mapped_column(default=0)
    strikeouts: Mapped[int] = mapped_column(default=0)
    stolen_bases: Mapped[int] = mapped_column(default=0)
    caught_stealing: Mapped[int] = mapped_column(default=0)

    #Relationships
    player: Mapped["Player"] = relationship(back_populates="batting_stats")
    game: Mapped["Game"] = relationship(back_populates="batter_stats")