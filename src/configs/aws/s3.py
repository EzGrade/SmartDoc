from typing import Annotated

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from configs.base import BaseConfig


class AwsEnvConfig(BaseConfig):
    VERBOSE_LOGGING: Annotated[bool | None, Field()] = False
    TARGET_REGION: Annotated[str, Field()] = "us-east-2"

    PROFILE: Annotated[str | None, Field()] = None
    ACCESS_KEY_ID: Annotated[str | None, Field()] = None
    SECRET_ACCESS_KEY: Annotated[str | None, Field()] = None

    CW_METRICS_NAMESPACE: Annotated[str | None, Field()] = "default-namespace"
    CW_NAMESPACE_POSTFIX: Annotated[str | None, Field()] = ""
    CW_RUNTIME_METRICS_ENABLED: Annotated[bool | None, Field()] = False

    model_config = SettingsConfigDict(env_prefix="AWS_")
