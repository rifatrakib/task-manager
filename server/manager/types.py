import re
from datetime import datetime
from typing import Callable, Dict, Generator, TypeAlias, TypeVar, Union
from uuid import UUID

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from pydantic import BaseModel, EmailStr
from pydantic.datetime_parse import parse_datetime

from server.manager.utils import as_utc, get_timestamp, get_utc_timezone

ObjectsVar = TypeVar("ObjectsVar", bound=Dict[str, Union[None, int, float, str, dict, list]])
StrOrNone: TypeAlias = Union[str, None]
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class StringUUID(str):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[str], str], None, None]:
        """Run validate class method."""
        yield cls.validate

    @classmethod
    def validate(cls, v) -> str:
        """Validate UUID object and convert it to string."""
        if isinstance(v, UUID):
            return str(v)

        try:
            result = UUID(v)
        except ValueError as error:
            raise ValueError("Invalid UUID") from error
        else:
            return str(result)


class Timestamp(float):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[str], str], None, None]:
        """Run validation class methods."""
        yield parse_datetime
        yield cls.ensure_has_timezone
        yield cls.to_timestamp

    @classmethod
    def ensure_has_timezone(cls, v: datetime) -> datetime:
        """Make naive datetime a timezone aware (with UTC timezone)."""
        if v.tzinfo is None:
            return v.replace(tzinfo=get_utc_timezone())
        else:
            return as_utc(date_time=v)

    @classmethod
    def to_timestamp(cls, v: datetime) -> Union[float, int]:
        """Convert datetime value to timestamp float."""
        return get_timestamp(v)

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        """Update type OpenAPIv3 schema."""
        field_schema.update(example=1656080975146.785, examples=[1656080947257.345, 1656080975146])


class Phone(str):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[str], str], None, None]:
        """Run validate class method."""
        yield cls.validate

    @classmethod
    def validate(cls, v: str) -> str:
        prefix = "+"
        if not re.match(r"^\d{8,15}$", v):
            raise ValueError("Must be digits")

        try:
            v = "".join((digit for digit in v if digit.isdigit()))  # format phone (allow only digits)
            v = prefix + v
            parsed_phone = phonenumbers.parse(v, None)
        except NumberParseException as error:
            raise ValueError("Invalid phone number") from error
        else:
            if phonenumbers.is_possible_number(parsed_phone):
                return v.removeprefix(prefix)

        raise ValueError("Impossible Number")

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        """Update type OpenAPIv3 schema."""
        field_schema.update(
            title="Phone number",
            max_length=15,
            example="380978531216",
            examples=["380978531216", "380978531226"],
        )


class Email(EmailStr):
    """Lowercase version of Pydantic EmailStr field type."""

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[str], str], None, None]:
        """Add extra validator to Pydantic EmailStr field."""
        yield from super().__get_validators__()
        yield cls.lowercase

    @classmethod
    def lowercase(cls, v: str) -> str:
        """Lowercase email value.

        Returns:
            value (str): lowercase value of email.
        """
        return v.lower()
