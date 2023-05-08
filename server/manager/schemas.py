from datetime import datetime, timedelta
from uuid import UUID

import orjson
import pydantic
from pydantic import BaseModel

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
