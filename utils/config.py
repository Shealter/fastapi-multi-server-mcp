import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Keys
    openweather_api_key: Optional[str] = None
    news_api_key: Optional[str] = None
    exchange_rates_api_key: Optional[str] = None

    # Server Configuration
    port: int = 10000
    host: str = "0.0.0.0"
    log_level: str = "info"

    class Config:
        env_file = ".env"


settings = Settings()
