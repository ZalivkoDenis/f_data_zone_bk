from pydantic import Field, PostgresDsn

from core.models import MainSettings


class DbSettings(MainSettings):
    url: PostgresDsn = Field(alias="MAIN_DB_PATH")
    echo: bool = Field(alias="MAIN_DB_ECHO", default=False)


class Settings(MainSettings):
    api_v1_prefix: str = Field(default="/api/v1")
    db: DbSettings = DbSettings()


settings = Settings()
db_settings = DbSettings()
