from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

# DB_PATH = BASE_DIR / "db.sqlite3"
DB_PATH = "postgresql+psycopg_async://postgres:xthnjgjkj[@127.0.0.1/dz"


class DbSettings(BaseModel):
    url: str = f"{DB_PATH}"
    # echo: bool = False
    echo: bool = False


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()


settings = Settings()
