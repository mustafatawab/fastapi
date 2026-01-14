from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"



@lru_cache
def get_settings() -> Settings:
    return Settings()