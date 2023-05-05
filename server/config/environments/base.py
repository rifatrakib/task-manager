from pydantic import BaseSettings, Extra, PostgresDsn


class AppConfig(BaseSettings):
    class Config:
        env_file = "configurations/.env"
        env_file_encoding = "UTF-8"
        env_nested_delimiter = "__"
        extra = Extra.forbid


class BaseConfig(AppConfig):
    APP_NAME: str
    RDS_URL: PostgresDsn
