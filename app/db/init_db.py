from app.db.session import engine
from app.models.base import Base

from app.models import game, player, team

def init_db():
    print("Creating tables..")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    init_db()