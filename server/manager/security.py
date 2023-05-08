import secrets
from datetime import datetime, timedelta
from typing import Dict, Sequence, Type, TypeAlias, Union

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from server.config.factory import settings
from server.manager.enums import TokenAudience
from server.manager.exceptions import ServerException
from server.manager.schemas import TokenOptionsSchema
from server.manager.utils import utc_now

DatetimeOrNone: TypeAlias = Union[datetime, None]


class HashGenerator:
    def __init__(self):
        self._hash_ctx_layer_1: CryptContext = CryptContext(
            schemes=[settings.HASHING_ALGORITHM_LAYER_1], deprecated="auto"
        )
        self._hash_ctx_layer_2: CryptContext = CryptContext(
            schemes=[settings.HASHING_ALGORITHM_LAYER_2], deprecated="auto"
        )
        self._hash_ctx_salt: str = settings.HASHING_SALT

    @property
    def _get_hashing_salt(self) -> str:
        return self._hash_ctx_salt

    @property
    def generate_password_salt_hash(self) -> str:
        """A function to generate a hash from Bcrypt to append to the user
        password."""
        return self._hash_ctx_layer_1.hash(secret=self._get_hashing_salt)

    def generate_password_hash(self, hash_salt: str, password: str) -> str:
        """A function that adds the user's password with the layer 1 Bcrypt
        hash, before hash it for the second time using Argon2 algorithm."""
        return self._hash_ctx_layer_2.hash(secret=hash_salt + password)

    def is_password_verified(self, password: str, hash_salt: str, hashed_password: str) -> bool:
        """A function that decodes users' password and verifies whether it is
        the correct password."""
        return self._hash_ctx_layer_2.verify(secret=hash_salt + password, hash=hashed_password)


def get_hash_generator() -> HashGenerator:
    return HashGenerator()


hash_generator: HashGenerator = get_hash_generator()


class PasswordManager:
    @staticmethod
    def generate_salt() -> str:
        return hash_generator.generate_password_salt_hash

    @staticmethod
    def make_password(*, password: str, hash_salt: str) -> str:
        return hash_generator.generate_password_hash(hash_salt=hash_salt, password=password)

    @staticmethod
    def verify_password(*, password: str, hash_salt: str, hashed_password: str) -> bool:
        return hash_generator.is_password_verified(
            password=password,
            hash_salt=hash_salt,
            hashed_password=hashed_password,
        )

    @staticmethod
    def generate_password(*, length: int = 8) -> str:
        return secrets.token_urlsafe(nbytes=length)


class TokenManager:
    @staticmethod
    def create_code(
        *,
        data: Dict[str, Union[str, int, float, dict, list, bool, None]] = None,
        aud: TokenAudience = TokenAudience.ACCESS,
        iat: DatetimeOrNone = None,
        exp: DatetimeOrNone = None,
        nbf: DatetimeOrNone = None,
        iss: str = settings.TOKEN_ISSUER,
    ) -> str:
        if data is None:
            data = {}

        now = utc_now()
        if iat is None:
            iat = now

        default_token_lifetime: timedelta = timedelta(minutes=settings.TOKEN_LIFETIME_MINUTES)
        if exp is None:
            exp = now + default_token_lifetime

        if nbf is None:
            nbf = now

        payload = data.copy()
        payload |= {"iat": iat, "aud": aud.value, "exp": exp, "nbf": nbf, "iss": iss}
        return jwt.encode(payload=payload, key=settings.JWT_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)

    @staticmethod
    def read_code(
        *,
        code: str,
        aud: Union[TokenAudience, Sequence[TokenAudience]] = TokenAudience.ACCESS,
        iss: str = settings.TOKEN_ISSUER,
        leeway: int = 0,
        convert_to: Union[Type[BaseModel], None] = None,
        options: Union[TokenOptionsSchema, None] = None,
    ):
        try:
            options = options or TokenOptionsSchema()
            audience = [item.value for item in aud] if isinstance(aud, (set, list, tuple)) else aud.value

            payload: Dict[str, Union[int, float, str, dict, list, bool]] = jwt.decode(
                jwt=code,
                key=settings.JWT_SECRET_KEY,
                algorithm=settings.TOKEN_ALGORITHM,
                audience=audience,
                issuer=iss,
                options=options.dict().update({"leeway": leeway}),
            )

            if convert_to:
                payload = convert_to(**payload)
        except JWTError as error:
            raise ServerException(message=error.args[0]) from error
        else:
            return payload
