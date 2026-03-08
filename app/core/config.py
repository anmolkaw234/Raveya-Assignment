from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Rayeva AI Systems Assignment"
    app_env: str = "development"
    debug: bool = True
    database_url: str = "sqlite:///./rayeva.db"

    ai_provider: str = "openai_compatible"
    ai_model: str = "llama-3.3-70b-versatile"
    ai_api_key: str = "replace_me"
    ai_base_url: str = "https://api.groq.com/openai/v1"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
