from pydantic import BaseSettings, Extra, PostgresDsn


class AppConfig(BaseSettings):
    class Config:
        env_file = "configurations/.env"
        env_file_encoding = "UTF-8"
        env_nested_delimiter = "__"
        extra = Extra.forbid


class BaseConfig(AppConfig):
    # general
    APP_NAME: str

    # hashing
    HASHING_ALGORITHM_LAYER_1: str
    HASHING_ALGORITHM_LAYER_2: str
    HASHING_SALT: str

    # token
    JWT_SECRET_KEY: str
    TOKEN_ALGORITHM: str
    TOKEN_ISSUER: str
    TOKEN_LIFETIME_SECONDS: int
    TOKEN_LIFETIME_MINUTES: int
    TOKEN_LIFETIME_HOURS: int
    TOKEN_LIFETIME_DAYS: int

    # database
    RDS_URL: PostgresDsn
