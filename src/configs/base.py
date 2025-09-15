from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class BaseConfig(BaseModel):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8"
    )
