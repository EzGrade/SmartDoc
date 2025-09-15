from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
