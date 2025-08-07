from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.models.base import Base
from app.models import Player, Game

class FielderGameStats(Base):
    __tablename__ = "fielder_game_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), nullable=False)
  
    position: Mapped[str] = mapped_column(nullable=True)
    putouts: Mapped[int] = mapped_column(default=0)
    assists: Mapped[int] = mapped_column(default=0)
    errors: Mapped[int] = mapped_column(default=0)
    double_plays_turned: Mapped[int] = mapped_column(default=0)
    fielding_chances: Mapped[int] = mapped_column(default=0)


    #Relationships
    player: Mapped["Player"] = relationship(back_populates="fielding_stats")
    game: Mapped["Game"] = relationship(back_populates="fielder_stats")