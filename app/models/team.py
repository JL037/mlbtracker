from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from sqlalchemy import ForeignKey
from datetime import date

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str]
    abbreviation: Mapped[str | None] = mapped_column(nullable=True)
    location: Mapped[str | None] = mapped_column(nullable=True)
    league: Mapped[str | None] = mapped_column(nullable=True)
    division: Mapped[str | None] = mapped_column(nullable=True)
    