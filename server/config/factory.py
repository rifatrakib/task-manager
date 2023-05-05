from functools import lru_cache

from decouple import config

from server.config.environments.base import BaseConfig
from server.config.environments.development import DevelopmentConfig
from server.config.environments.production import ProductionConfig
from server.config.environments.staging import StagingConfig


class SettingsFactory:
    def __init__(self, mode: str):
        self.mode = mode

    def __call__(self) -> BaseConfig:
        if self.mode == "staging":
            return StagingConfig()
        elif self.mode == "production":
            return ProductionConfig()
        else:
            return DevelopmentConfig()


@lru_cache()
def get_settings() -> SettingsFactory:
    return SettingsFactory(mode=config("MODE", default="development", cast=str))()


settings: BaseConfig = get_settings()
