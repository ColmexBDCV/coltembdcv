from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./coltem_v2.db"

settings = Settings()