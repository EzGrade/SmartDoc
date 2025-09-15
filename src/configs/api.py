from typing import Literal

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from configs.base import BaseConfig


class ApiConfig(BaseConfig):
    TITLE: str = Field(default="API", description="API title")
    VERSION: Literal["1"] = Field(default="1", description="API version")
    DEBUG: bool = Field(default=False, description="Debug mode")

    model_config = SettingsConfigDict(
        env_prefix="API_",
    )
