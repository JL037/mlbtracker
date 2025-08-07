from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    game_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    date: Mapped[datetime]
    status: Mapped[str | None] = mapped_column(nullable=True)
    location: Mapped[str | None] = mapped_column(nullable=True)

    scheduled_start_time: Mapped[datetime | None] = mapped_column(nullable=True)
    official_start_time: Mapped[datetime | None] = mapped_column(nullable=True)
    game_duration: Mapped[str | None] = mapped_column(nullable=True)
    calculated_end_time: Mapped[datetime | None] = mapped_column(nullable=True)
    
    temperature: Mapped[str | None] = mapped_column(nullable=True)
    weather_condition: Mapped[str | None] = mapped_column(nullable=True)
    wind: Mapped[str | None] = mapped_column(nullable=True)
    
    
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    
    home_team: Mapped["Team"] = relationship(foreign_keys=[home_team_id], back_populates="home_games")
    away_team: Mapped["Team"] = relationship(foreign_keys=[away_team_id], back_populates="away_games")
    