from datetime import date, datetime
from functools import lru_cache, partial
from typing import Any, Callable, Dict
from uuid import uuid1, uuid4
from zoneinfo import ZoneInfo

import orjson
from fastapi.encoders import jsonable_encoder
from pydash import camel_case


@lru_cache()
def get_utc_timezone() -> ZoneInfo:
    """Return UTC zone info."""
    return ZoneInfo(key="UTC")


def utc_now() -> datetime:
    """Return current datetime with UTC zone info."""
    return datetime.now(tz=get_utc_timezone())


def as_utc(date_time: datetime) -> datetime:
    """Get datetime object and convert it to datetime with UTC zone info."""
    return date_time.astimezone(tz=get_utc_timezone())


def id_v1() -> str:
    """Generate UUID with version 1 (can extract created_at datetime)."""
    return str(uuid1())


def id_v4() -> str:
    """Generate UUID with version 4."""
    return str(uuid4())


def orjson_dumps(v: Any, *, default: Any) -> str:
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode(encoding="utf-8")


def get_timestamp(v: datetime) -> float:
    """Extract timestamp from datetime object and round for 3 decimal
    digits."""
    return round(v.timestamp() * 1000, 3)


def proxy_func(x: Any) -> Any:
    """Function that proxies value back (doing nothing)."""
    return x


def to_camel_case(key: str) -> str:
    return camel_case(key)


encodings_dict: Dict[Any, Callable[[Any], Any]] = {
    datetime: proxy_func,  # don't transform datetime objects
    date: proxy_func,  # don't transform date objects
}

to_db_encoder = partial(
    jsonable_encoder,
    exclude_unset=True,
    by_alias=False,
    custom_encoder=encodings_dict,  # override `jsonable_encoder` default behaviour
)
