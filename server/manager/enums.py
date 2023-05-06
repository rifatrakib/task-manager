from enum import Enum


class ClientEndStatus(str, Enum):
    """Enum based class to set type of client side statuses."""

    ERROR = "error"
    FAIL = "fail"
    SUCCESS = "success"


class TokenAudience(str, Enum):
    """Enum based class to set type of JWT."""

    ACCESS = "access"
    REFRESH = "refresh"


class FilterOps(str, Enum):
    """Enum for Filter Operations."""

    EQUAL = "="
    NOT_EQUAL = "!="
    GREATER = ">"
    LESS = "<"
    GREATER_OR_EQUAL = ">="
    LESS_OR_EQUAL = "<="
    IN = "in"
    NOT_IN = "notin"
    LIKE = "like"
    ILIKE = "ilike"
    STARTSWITH = "startswith"
    ENDSWITH = "endswith"
    ISNULL = "isnull"
    NOT_NULL = "notnull"

    # Aliases
    EQ = EQUAL
    NE = NOT_EQUAL
    G = GREATER
    GE = GREATER_OR_EQUAL
    L = LESS
    LE = LESS_OR_EQUAL


class RatePeriod(str, Enum):
    """Predefined periods for RateLimiters.

    Used in datetime.timedelta constructor.
    """

    SECOND = "seconds"
    MINUTE = "minutes"
    HOUR = "hours"
    DAY = "days"
    WEEK = "weeks"
