from hashlib import pbkdf2_hmac
from hmac import compare_digest

from infra.constants._string import GenericConstants


class HashGenerator():
    HASH_NAME_SHA_256 = "sha256"

    @staticmethod
    def create(
        value: str,
        salt: str,
        iterations: int = 100
    ) -> str:
        return pbkdf2_hmac(
            hash_name=HashGenerator.HASH_NAME_SHA_256,
            password=value.encode(encoding=GenericConstants.UTF8),
            salt=salt.encode(encoding=GenericConstants.UTF8),
            iterations=iterations,
            dklen=None
        ).hex()

    @staticmethod
    def is_valid(
        hashed_value: str,
        value: str,
        salt: str,
        iterations: int = 100
    ) -> bool:
        return compare_digest(
            hashed_value, HashGenerator.create(
                value=value, salt=salt, iterations=iterations)
        )
