from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BizSC"

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    edinet_api_key: Optional[str] = None # str | Noneと同じ意味

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()