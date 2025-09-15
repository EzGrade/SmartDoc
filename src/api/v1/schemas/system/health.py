from pydantic import Field

from ..base import BaseSchema


class HealthResponseSchema(BaseSchema):
    status: str = Field(default="success", description="Health status")
