from functools import lru_cache
from typing import Literal

from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration, read from environment variables (and `.env` locally).

    Required fields have no default: if one is missing, startup fails immediately
    with a clear validation error instead of crashing later inside a request.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # unrelated env vars (PATH, HOME...) are not errors
        env_ignore_empty=True,  # `GITHUB_TOKEN=` means "not set", not an empty secret
    )

    environment: Literal["local", "test", "production"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    database_url: PostgresDsn
    secret_key: SecretStr

    app_base_url: str = "http://localhost:3000"

    # Optional until the milestones that need them
    github_token: SecretStr | None = None
    resend_api_key: SecretStr | None = None


@lru_cache
def get_settings() -> Settings:
    """Build Settings once per process. Tests call `get_settings.cache_clear()` to reload."""
    return Settings()
