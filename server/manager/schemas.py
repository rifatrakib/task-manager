from datetime import datetime, timedelta
from typing import Generic, List, Union
from uuid import UUID

import orjson
import pydantic
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

from server.manager.enums import ClientEndStatus
from server.manager.types import SchemaType, StrOrNone
from server.manager.utils import get_timestamp, orjson_dumps


class BaseInSchema(BaseModel):
    """Base schema for schemas that will be used in request validations."""

    class Config:
        """Configuration for the base input schema."""

        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        orm_mode = True
        use_enum_values = True
        validate_assignment = True


class BaseOutSchema(BaseInSchema):
    """Base schema for schemas that will be used in responses."""

    class Config:
        """Configuration for the base output schema."""

        json_encoders = {
            datetime: get_timestamp,
            timedelta: lambda time_delta: pydantic.json.timedelta_isoformat(time_delta),
            UUID: str,
        }
        json_dumps = orjson_dumps
        json_loads = orjson.loads


class ClientOutSchema(GenericModel, Generic[SchemaType]):
    """Client side output schema."""

    status: ClientEndStatus = Field(default=ClientEndStatus.SUCCESS)
    data: Union[SchemaType, None] = Field(default=None)
    message: str = Field(default=...)
    code: int = Field(default=status.HTTP_200_OK)


class UnprocessableEntityOutSchema(BaseOutSchema):
    """Schema that uses in pydantic validation errors."""

    location: List[str] = Field(example=["body", "field_1"])
    message: str = Field(default="Field required.")
    type: str = Field(default="value_error.missing")
    context: StrOrNone = Field(default=None)
