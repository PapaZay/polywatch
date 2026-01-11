from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    POLYMARKET_GAMMA_API_URL: str = "https://gamma-api.polymarket.com"
    POLYMARKET_CLOB_API_URL:  str = "https://clob.polymarket.com"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()