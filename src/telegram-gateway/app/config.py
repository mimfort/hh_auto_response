from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    MODE: Literal["development", "production", "testing"] = "development"
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TELEGRAM_BOT_TOKEN: str
    SECRET_KEY: str
    SUPERUSER_ID: int
    