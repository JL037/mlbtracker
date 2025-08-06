from pydantic_settings import BaseSettings
import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")


class Settings(BaseSettings):
    POSTGRES_PORT: int
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    DATABASE_URL: str

Settings = Settings()