from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",env_file_encoding="utf-8",extra="ignore")
    app_name:str="CampusOS"; environment:str="development"; debug:bool=False
    database_url:str="postgresql+psycopg://campusos:campusos@postgres:5432/campusos"
    redis_url:str="redis://redis:6379/0"; jwt_secret:str=Field(min_length=32,default="change-this-development-secret-key-now")
    access_token_minutes:int=15; refresh_token_days:int=7
    cors_origins:str="http://localhost:3000,http://localhost:5173"
    gemini_api_key:str=""; gemini_model:str="gemini-2.0-flash"
    @property
    def allowed_origins(self): return [x.strip() for x in self.cors_origins.split(",") if x.strip()]
@lru_cache
def get_settings(): return Settings()
settings=get_settings()
