from pydantic import Field, PostgresDsn

from core.models import MainSettings


class DbSettings(MainSettings):
    url: str = Field(alias="MAIN_DB_PATH")
    echo: bool = Field(alias="MAIN_DB_ECHO", default=False)


class Settings(MainSettings):
    api_v1_prefix: str = Field(default="/api/v1")
    db: DbSettings = DbSettings()


settings = Settings()
db_settings = DbSettings()


# TEST
if __name__ == "__main__":
    # print(settings.api_v1_prefix)
    print(settings.db.url)

    # print(settings.db.echo)
    # print(db_settings.url)
    # print(db_settings.echo)
