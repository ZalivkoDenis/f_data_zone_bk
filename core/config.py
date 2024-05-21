from pathlib import Path

from pydantic import Field, PostgresDsn, BaseModel

from core.models.settings import MainSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class AuthJWT(BaseModel):
    private_key_path: str = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: str = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class DbSettings(MainSettings):
    url: str = Field(alias="MAIN_DB_PATH")
    echo: bool = Field(alias="MAIN_DB_ECHO", default=False)


class Settings(MainSettings):
    api_v1_prefix: str = Field(default="/api/v1")
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
db_settings = DbSettings()


# TEST
if __name__ == "__main__":
    # print(settings.api_v1_prefix)
    print(settings.db.url)

    # print(settings.db.echo)
    # print(db_settings.url)
    # print(db_settings.echo)
