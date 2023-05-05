from server.config.environments.base import BaseConfig


class ProductionConfig(BaseConfig):
    DEBUG: bool = True
    MODE: str = "production"

    class Config:
        env_file = ".env.production"
