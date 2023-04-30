from pydantic import BaseSettings


class Config(BaseSettings):
    TELEGRAM_TOKEN: str

    DB_NAME: str

    ADMIN_ID: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


config = Config()
