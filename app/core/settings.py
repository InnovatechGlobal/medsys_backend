# type: ignore
import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """The settings for the application."""

    model_config = SettingsConfigDict(env_file=".env")

    # App
    DEBUG: bool = os.environ.get("DEBUG")
    OAUTH2_STATE_EXPIRE_MIN: int = os.environ.get("OAUTH2_STATE_EXPIRE_MIN")
    MEDIA_DIR: str = os.environ.get("MEDIA_DIR")

    # Security
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    REFRESH_TOKEN_EXPIRE_HOURS: int = os.environ.get("REFRESH_TOKEN_EXPIRE_HOURS")
    ACCESS_TOKEN_EXPIRE_MINS: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINS")

    # Criipto
    CRIIPTO_VERIFY_DOMAIN: str = os.environ.get("CRIIPTO_VERIFY_DOMAIN")
    CRIIPTO_VERIFY_CLIENT_ID: str = os.environ.get("CRIIPTO_VERIFY_CLIENT_ID")
    CRIIPTO_VERIFY_CLIENT_SECRET: str = os.environ.get("CRIIPTO_VERIFY_CLIENT_SECRET")

    # OpenAI
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")

    # DB Settings
    POSTGRES_DATABASE_URL: str = os.environ.get("POSTGRES_DATABASE_URL")


@lru_cache
def get_settings():
    """This function returns the settings obj for the application."""
    return Settings()
