from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError, NoResultFound

from server.config.factory import settings
from server.manager.enums import ClientEndStatus
from server.manager.exceptions import RateLimitException, ServerException


def server_exception_handler(request: Request, exc: ServerException) -> ORJSONResponse:
    """Handler for ServerException.

    Args:
        request (Request): FastAPI Request instance.
        exc (ServerException): Error that backend raises.

    Returns:
        result (ORJSONResponse): Transformed JSON response from backend exception.
    """
    return ORJSONResponse(content=exc.dict(), status_code=exc.code)


def validation_exception_handler(request: Request, exc: RequestValidationError) -> ORJSONResponse:
    """Handler for RequestValidationError. Get the original 'detail' list of
    errors wrapped with client end structure.

    Args:
        request (Request): FastAPI Request instance.
        exc (RequestValidationError): Error that Pydantic raises (in case of validation error).

    Returns:
        result (ORJSONResponse): Transformed JSON response from backend exception.
    """
    errors = exc.errors()
    details = []
    for error in errors:
        details.append(
            {
                "location": error["loc"],
                "message": error["msg"].capitalize() + ".",
                "type": error["type"],
                "context": error.get("ctx", None),
            },
        )

    return ORJSONResponse(
        content={
            "status": ClientEndStatus.FAIL,
            "data": details,
            "message": "Validation error.",
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def integrity_error_handler(error: IntegrityError) -> None:
    """Handler for IntegrityError (SQLAlchemy error).

    Args:
        error (IntegrityError): Error that SQLAlchemy raises (in case of SQL query error).

    Raises:
        ServerException: Actually proxies these errors to `server_exception_handler`.
    """
    if "duplicate" in error.args[0]:
        raise ServerException(
            message=str(error.orig.args[0].split("\n")[-1]) if settings.DEBUG else "Update error.",
        )
    else:
        raise ServerException(
            message=str(error) if settings.DEBUG else "Internal server error.",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=ClientEndStatus.ERROR,
        )


def no_result_found_handler(error: NoResultFound) -> None:
    """Handler for NoResultFound (SQLAlchemy error).

    Args:
        error (NoResultFound): Error that SQLAlchemy raises (in case of scalar_one() error).

    Raises:
        ServerException: Actually proxies these errors to `server_exception_handler`.
    """
    raise ServerException(
        message="Not found.",
        code=status.HTTP_404_NOT_FOUND,
        status=ClientEndStatus.FAIL,
    )


def rate_limit_exception_handler(request: Request, exc: RateLimitException) -> ORJSONResponse:
    """Handler for RateLimitException.

    Args:
        request (Request): FastAPI Request instance.
        exc (RateLimitException): Error that RateLimiter raises.

    Returns:
        result (ORJSONResponse): Transformed JSON response from backend exception.
    """
    return ORJSONResponse(content=exc.dict(), status_code=exc.code, headers=exc.headers)
