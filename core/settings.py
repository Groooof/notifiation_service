import pydantic as pd


class Settings(pd.BaseSettings):
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    SENDER_TOKEN: str

    class Config:
        env_file = './core/.env'
        env_file_encoding = 'utf-8'


settings = Settings()
