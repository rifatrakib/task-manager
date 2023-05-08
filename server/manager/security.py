import secrets
from datetime import datetime
from typing import TypeAlias, Union

from passlib.context import CryptContext

from server.config.factory import settings

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
