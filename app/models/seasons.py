from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models import Game
class Season(Base):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(unique=True, nullable=False)


    #Relationships
    games: Mapped[list["Game"]] = relationship(back_populates="season")