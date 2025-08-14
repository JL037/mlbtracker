

---

##  1. Project Setup

- [x] Create and activate virtual environment
- [x] Install required packages (`pip install -r requirements.txt`)
- [x] Create `.env` file with database credentials and secret keys
- [x] Initialize git repository
- [x] Create `.gitignore` and add virtualenv, `.env`, `__pycache__`, etc.

---

##  2. Config Setup

- [x] Implement `config.py` to load env vars with `pydantic.BaseSettings`
- [x] Add environment variable validation and defaults
- [x] Hook up config in `main.py` and `db/session.py`

---

##  3. Database & ORM Setup

- [x] Implement `session.py` to create SQLAlchemy `SessionLocal` and `engine`
- [x] Implement `init_db.py` to run initial table creation from models
- [x] Set up `base.py` with `DeclarativeBase` for models

---

##  4. Models

### `models/player.py`
- [x] Define `Player` model with fields: id, name, team_id, position, stats, etc.
- [x] Add SQLAlchemy relationships (e.g., to `Team`)

### `models/team.py`
- [x] Define `Team` model with fields: id, name, location, abbreviation, etc.
- [x] Add reverse relationships to players and games

### `models/game.py`
- [x] Define `Game` model with fields: id, date, home_team_id, away_team_id, scores, etc.
- [x] Add relationships to `Team` and `Player`

---

##  5. ETL Pipeline

### `etl/fetch_data.py`
- [x] Implement logic to call external API or load from CSV
- [ ] Add logging and error handling for fetch process

### `etl/transform.py`
- [x] Write data normalization and parsing functions
- [ ] Clean and validate raw data

### `etl/load.py`
- [x] Insert transformed data into database via SQLAlchemy
- [x] Use sessions/transactions for batch inserts

---

##  6. API Endpoints

### `api/players.py`
- [ ] Create `GET /players/` endpoint (list all)
- [ ] Create `GET /players/{id}` (player by ID)
- [ ] Create `POST /players/` (create player)
- [ ] Create `PUT /players/{id}` (update player)
- [ ] Create `DELETE /players/{id}` (delete player)

### `api/teams.py`
- [ ] Create `GET /teams/`
- [ ] Create `GET /teams/{id}`
- [ ] Create `POST /teams/`
- [ ] Create `PUT /teams/{id}`
- [ ] Create `DELETE /teams/{id}`

### `api/games.py`
- [ ] Create `GET /games/`
- [ ] Create `GET /games/{id}`
- [ ] Create `POST /games/`
- [ ] Create `PUT /games/{id}`
- [ ] Create `DELETE /games/{id}`

---

##  7. Main App Entry

- [ ] Implement `main.py` to create FastAPI app instance
- [ ] Include routers from all API files
- [ ] Add CORS middleware (if needed)
- [ ] Add global exception handlers (optional)

---

##  8. Testing (optional)

- [ ] Set up `tests/` directory
- [ ] Add test DB config
- [ ] Write unit tests for each model (player, team, game)
- [ ] Write endpoint tests using FastAPI TestClient

---

##  9. Docker Setup (optional)

- [ ] Create `Dockerfile` for FastAPI app
- [ ] Create `docker-compose.yml` with Postgres service
- [ ] Mount volume for database persistence
- [ ] Configure `.env` to work inside Docker

---

##  10. Documentation

- [ ] Add API documentation with tags and descriptions
- [ ] Enable `/docs` and `/redoc` endpoints
- [ ] Update `README.md` with setup instructions, API usage, and examples
- [ ] Add ERD (Entity Relationship Diagram) to README

---

##  11. Alembic Migrations

- [ ] Run `alembic init alembic`
- [ ] Configure `alembic.ini` with DB URL from `.env`
- [ ] Add `env.py` logic to import `Base` from `models.base`
- [ ] Create and apply first migration

---

##  Done?

Once all the above tasks are complete, you’ll have:

- Full working backend
- ETL job pulling real MLB data
- CRUD-ready API for Players, Teams, Games
- Containerized infrastructure (if Docker enabled)
- Swagger & Redoc API docs

---

###  Optional Enhancements

- [ ] Add search/filtering to endpoints
- [ ] Add pagination to list views
- [ ] Add rate limiting/middleware
- [ ] Schedule ETL runs using `APScheduler` or `cron`

##  Project Goals

- Pull MLB data for teams, games, players, and stats using the free **MLB-StatsAPI**
- Store it in a structured **PostgreSQL** database
- Build an **ETL pipeline** to refresh the data regularly (hourly/daily)
- Create a **FastAPI** backend to expose the data
- Optionally add a **fun frontend** (React or Svelte) for stat exploration

---

##  Phase 1: Project Setup

### 1. Initialize Git + Repo

```bash
mkdir mlb-stats-tracker
cd mlb-stats-tracker
git init
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

### 3. Install required packages

```bash
pip install fastapi uvicorn requests sqlalchemy psycopg2-binary pandas pydantic
pip install python-dotenv
```

Create `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

##  Phase 2: Project Structure

```
mlb-stats-tracker/
├── app/
│   ├── main.py
│   ├── etl/
│   │   ├── __init__.py
│   │   ├── fetch_data.py
│   │   ├── transform.py
│   │   ├── load.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── game.py
│   │   ├── team.py
│   │   └── player.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── games.py
│   │   ├── players.py
│   │   └── teams.py
│   ├── db/
│   │   ├── session.py
│   │   └── init_db.py
│   └── config.py
├── .env
├── requirements.txt
├── README.md
└── alembic/
```

---

##  Phase 3: Database Setup

### 1. Create `.env`

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=mlbstats
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 2. Setup PostgreSQL (with Docker)

**docker-compose.yml**

```yaml
version: "3.8"
services:
  db:
    image: postgres
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run:

```bash
docker-compose up -d
```

---

##  Phase 4: Build the ETL Pipeline

### `etl/fetch_data.py`

```python
import requests

def fetch_games(date: str):
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date}"
    response = requests.get(url)
    return response.json()
```

### `etl/transform.py`

```python
def transform_games(raw_data):
    games = []
    for date in raw_data["dates"]:
        for game in date["games"]:
            games.append({
                "game_id": game["gamePk"],
                "home_team": game["teams"]["home"]["team"]["name"],
                "away_team": game["teams"]["away"]["team"]["name"],
                "status": game["status"]["detailedState"],
                "date": game["gameDate"]
            })
    return games
```

### `etl/load.py`

```python
from app.db.session import SessionLocal
from app.models.game import Game

def load_games(data):
    db = SessionLocal()
    for item in data:
        db_game = Game(**item)
        db.add(db_game)
    db.commit()
    db.close()
```

---

##  Phase 5: Models (SQLAlchemy)

### `models/game.py`

```python
from sqlalchemy import Column, Integer, String, DateTime
from app.models.base import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, unique=True)
    home_team = Column(String)
    away_team = Column(String)
    status = Column(String)
    date = Column(DateTime)
```

### `models/base.py`

```python
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
```

---

##  Phase 6: API Endpoints (FastAPI)

### `api/games.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.game import Game

router = APIRouter()

@router.get("/games")
def get_games(db: Session = Depends(get_db)):
    return db.query(Game).all()
```

### `main.py`

```python
from fastapi import FastAPI
from app.api import games

app = FastAPI()

app.include_router(games.router, prefix="/api")
```

---

##  Phase 7: Run ETL as Scheduled Job

```python
import schedule
import time
from app.etl.fetch_data import fetch_games
from app.etl.transform import transform_games
from app.etl.load import load_games

def job():
    raw = fetch_games("2025-08-05")
    transformed = transform_games(raw)
    load_games(transformed)

schedule.every().day.at("12:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

##  Optional: Frontend (React)

- Hit `/api/games` using Axios or fetch
- Show a scoreboard, team stats, or player stats
- Use Chart.js or D3 for graphs
- Add animations or emojis for fun

---

##  Phase 8: Final Touches

- Swagger docs at `/docs` (FastAPI default)
- Set up Alembic for migrations
- Add unit tests with `pytest`
- Dockerize FastAPI backend
- Deploy backend to **Render**, **Fly.io**, or **Railway**
- Deploy frontend to **Vercel**, **Netlify**, or GitHub Pages

---

##  MLB StatsAPI Notes

- No API key required
- Endpoints:
  - `https://statsapi.mlb.com/api/v1/schedule`
  - `https://statsapi.mlb.com/api/v1/game/{gamePk}/boxscore`
  - `https://statsapi.mlb.com/api/v1/people/{playerId}/stats`
  - `https://statsapi.mlb.com/api/v1/teams`

---

##  Suggested Next Steps

- Expand models for `Team`, `Player`, `Stats`
- Add player search endpoint
- Add team standings and leaderboard logic
- Implement daily or hourly cron job

---