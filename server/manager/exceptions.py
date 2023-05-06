from typing import Any, Dict, List, Union

from fastapi import status

from server.manager.enums import ClientEndStatus


class ServerException(Exception):
    """Exception for Back-end with client end adaptation.

    Examples:
        >>> raise ServerException(
        ...     status=ClientEndStatus.SUCCESS,
        ...     data=["Something", "Interesting"],
        ...     message="Fascinating exception.",
        ...     code=http_status.HTTP_200_OK
        ... )
    """

    def __init__(
        self,
        *,
        status: ClientEndStatus = ClientEndStatus.FAIL,
        data: Union[None, int, str, List[Any], Dict[str, Any]] = None,
        message: str,
        code: int = status.HTTP_400_BAD_REQUEST,
    ):
        """Initializer for ServerException.

        Keyword Args:
            status (ClientEndStatus): status for client side.
            data: any detail or data for this exception.
            message (str): any text detail for this exception.
            code (int): HTTP status code or custom code from backend.
        """
        self.status = status
        self.data = data
        self.message = message
        self.code = code

    def __repr__(self) -> str:
        """Representation for ServerException."""
        return (
            f'{self.__class__.__name__}(status={self.status}, data={self.data}, message="{self.message}",'
            f" code={self.code})"
        )

    def __str__(self) -> str:
        """String representation for ServerException."""
        return self.__repr__()

    def dict(self) -> Dict[str, Any]:
        """Converts ServerException to python dict.

        Actually used to wrap ClientEndStatus response.
        """
        return {
            "status": self.status.value if isinstance(self.status, ClientEndStatus) else self.status,
            "data": self.data,
            "message": self.message,
            "code": self.code,
        }


class RateLimitException(ServerException):
    def __init__(
        self,
        *,
        status: ClientEndStatus = ClientEndStatus.FAIL,
        data: Union[None, int, str, List[Any], Dict[str, Any]] = None,
        message: str,
        code: int = status.HTTP_429_TOO_MANY_REQUESTS,
        headers: Dict[str, str] = None,
    ) -> None:
        super().__init__(status=status, data=data, message=message, code=code)
        self.headers = headers
