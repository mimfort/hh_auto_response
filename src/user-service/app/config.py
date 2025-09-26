from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Базовые настройки приложения"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    mode: str = "DEV"  # DEV, DEBUG, PRODUCTION
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str
    db_driver: str
    database_url: str
    log_level: str = "INFO"

    @property
    def is_debug(self) -> bool:
        """Проверяет, включен ли режим отладки"""
        return self.log_level.upper() == "DEBUG"

    @property
    def is_production(self) -> bool:
        """Проверяет, включен ли режим продакшн"""
        return self.log_level.upper() == "PRODUCTION"
