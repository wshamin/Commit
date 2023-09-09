import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    ALGORITHM: str = 'HS256'

    class Config:
        env_file = '../.env'


settings = Settings()