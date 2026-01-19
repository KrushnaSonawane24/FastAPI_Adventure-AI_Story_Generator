from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    DATABASE_URL: str = "sqlite:///./app.db"
    DEBUG: bool = True
    ALLOWED_ORIGINS: str = "*"
    GOOGLE_API_KEY: str = ""

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        if v == "*":
            return ["*"]
        return [origin.strip() for origin in v.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False  # Changed to False for easier .env loading

settings = Settings() 


























































































































































