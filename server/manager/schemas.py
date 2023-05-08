from datetime import datetime, timedelta
from typing import Any, Generic, List, Union
from uuid import UUID

import orjson
import pydantic
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

from server.manager.enums import ClientEndStatus
from server.manager.types import SchemaType, StrOrNone, Timestamp
from server.manager.utils import get_timestamp, orjson_dumps, to_camel_case


class BaseInSchema(BaseModel):
    """Base schema for schemas that will be used in request validations."""

    class Config:
        """Configuration for the base input schema."""

        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        orm_mode = True
        use_enum_values = True
        validate_assignment = True


class OutputAliasConfig(BaseModel):
    class Config:
        alias_generator: Any = to_camel_case


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


class CreatedAtOutSchema(OutputAliasConfig):
    """Schema with `createdAt` Timestamp field."""

    created_at: Timestamp = Field(title="Created at")


class UpdatedAtOutSchema(OutputAliasConfig):
    """Schema with `updatedAt` Timestamp field."""

    updated_at: Timestamp = Field(title="Updated at")


class WriteHistoryOutSchema(CreatedAtOutSchema, UpdatedAtOutSchema):
    """Schema with `createdAt` and `updatedAt` Timestamp fields."""


class TokenPayloadSchema(BaseOutSchema):
    """Base JWT token payloads."""

    iat: Timestamp
    aud: str
    exp: Timestamp
    nbf: Timestamp
    iss: str


class TokenOptionsSchema(BaseOutSchema):
    """Schema options for PyJWT parsing & validation."""

    verify_signature: bool = Field(default=True)
    require: List[str] = Field(default=["aud", "exp", "iat", "iss", "nbf"])
    verify_aud: bool = Field(default=True)
    verify_exp: bool = Field(default=True)
    verify_iat: bool = Field(default=True)
    verify_iss: bool = Field(default=True)
    verify_nbf: bool = Field(default=True)
