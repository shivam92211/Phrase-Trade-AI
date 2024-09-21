import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    class Config:
        env = os.environ.get("API_ENV")
        if env:
            print("Enviroment Loaded =>> ", env)
        env_file = ".env" if env == "production" else ".env.development"
        # Load environment variables
        load_dotenv(dotenv_path=env_file)

    # enviornment recognition 'development' | 'production'
    API_ENV: str

    GOOGLE_API_KEY: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str

    @property
    def POSTGRES_URL(self):
        url = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return url


env = Settings()
