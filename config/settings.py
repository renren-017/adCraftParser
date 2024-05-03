from pydantic_settings import BaseSettings

__all__ = ["settings"]


class Settings(BaseSettings):
    log_level: str = "DEBUG"
    log_file: str = "logs/app.log"
    log_max_bytes: int = 1024 * 1024 * 5  # 5 MB
    log_backup_count: int = 5
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_date_format: str = "%Y-%m-%d %H:%M:%S"

    GOOGLE_SEARCH_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
