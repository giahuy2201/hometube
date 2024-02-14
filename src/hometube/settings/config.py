import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    config_path:str = '/config'
    media_path:str = '/media'
    downloads_path:str = '/downloads'


settings = Settings()
