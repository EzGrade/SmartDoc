from pydantic import Field

from ..base import BaseSchema


class NetworkUploadAssetSchema(BaseSchema):
    uuid: str = Field(description="UUID of the asset")
