from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        extra="ignore",
        env_file_encoding="utf-8"
    )
