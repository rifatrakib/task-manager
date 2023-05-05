from functools import lru_cache

from pydantic import BaseSettings, Extra, PostgresDsn


class AppConfig(BaseSettings):
    APP_NAME: str
    MODE: str
    RDS_URL: PostgresDsn

    class Config:
        extra = Extra.forbid
        env_file = ".env"
        env_file_encoding = "UTF-8"
        env_nested_delimiter = "__"


@lru_cache()
def get_app_config():
    return AppConfig()


settings: AppConfig = get_app_config()
