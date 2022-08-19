import pydantic as pd


class Settings(pd.BaseSettings):
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    POSTGRES_DSN: str

    class Config:
        env_file = './core/storage/.env'
        env_file_encoding = 'utf-8'


settings = Settings()

