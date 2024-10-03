import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    class Config:
        env = os.environ.get("API_ENV")
        if env:
            print("Enviroment Loaded =>> ", env)
        env_file = ".env.production" if env == "production" else ".env.development"
        # Load environment variables
        load_dotenv(dotenv_path=env_file)

    # enviornment recognition 'development' | 'production'
    API_ENV: str

    GOOGLE_API_KEY: str
    PG_VECTOR_DB_USER: str
    PG_VECTOR_DB_PASSWORD: str
    PG_VECTOR_DB: str
    PG_VECTOR_DB_PORT: str
    PG_VECTOR_DB_HOST: str

    ALLOWED_ORIGINS: list[str]
    AI_BEARER_TOKEN: str

    @property
    def POSTGRES_URL(self):
        url = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return url


env = Settings()
