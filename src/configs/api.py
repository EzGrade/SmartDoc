from pydantic import Field

from configs.base import BaseConfig


class ApiConfig(BaseConfig):
    title: str = Field(default="API", description="API title")
    version: int = Field(default=1, description="API version")
    debug: bool = Field(default=False, description="Debug mode")
