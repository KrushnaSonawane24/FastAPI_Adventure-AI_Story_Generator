from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_PREFIX:str="/api"

    DATABASE_URL:str="sqlite:///./app.db"

    DEBUG:bool=True

    ALLOWED_ORIGINS:str=" "
    OPEN_AI_KEY:str=""

    @field_validator("ALLOWED_ORIGINS")#kyu ki ALLOW_ORIGINS me two link hai iske liye 
    def parse_allowed_origins(cls,v:str) -> List[str]:
        return v.split(",") if v else []# .env file me ALLOW_ORIGINS me two link hai jo " , " se seprate hai to ye hai to sahi hai agar nahi hai to empty list return karo 

    class Config:
        env_file =".env"
        env_file_encoding="utf-8"
        case_sensitive = True

settings = Settings()#jo bhi hamen likha hai vo sab setting me hai aab 


























































































































































