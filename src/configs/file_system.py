from pydantic import Field
from pydantic_settings import SettingsConfigDict

from configs.base import BaseSettings


class FileSystemConfig(BaseSettings):
    USE_AWS_S3: bool = Field(default=False, description="Use AWS S3 for file system")
    LOCAL_AWS_S3_PATH: str = Field(default="media", description="Local AWS S3 path")

    model_config = SettingsConfigDict(
        env_prefix="FS_",
    )