from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ai-agent-system"
    app_env: str = "dev"
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000
    allowed_tools: List[str] = ["summarize", "classify", "retrieve_context"]
    max_input_chars: int = 12000
    default_summary_sentences: int = 2

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @field_validator("allowed_tools", mode="before")
    @classmethod
    def parse_allowed_tools(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
