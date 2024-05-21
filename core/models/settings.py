from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


SETTINGS_BASE_DIR = Path(__file__).resolve().parent.parent.parent


class MainSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=SETTINGS_BASE_DIR / ".env", extra="ignore"
    )
