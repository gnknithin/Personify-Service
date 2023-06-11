from typing import Any, Dict

import jwt


class TokenGenerator():
    JWT_SECRET = "dummy-secret"
    JWT_ALGORITHM = "HS256"

    @staticmethod
    def encode(data: Dict[Any, Any]) -> str:

        return jwt.encode(
            payload=data,
            key=TokenGenerator.JWT_SECRET,
            algorithm=TokenGenerator.JWT_ALGORITHM,
            headers=None,
            json_encoder=None,
            sort_headers=True
        )

    @staticmethod
    def decode(value: str) -> Dict[Any, Any]:
        return jwt.decode(
            jwt=value,
            key=TokenGenerator.JWT_SECRET,
            algorithms=[TokenGenerator.JWT_ALGORITHM],
            options=None,
            verify=None,
            detached_payload=None,
            audience=None,
            issuer=None,
            leeway=0
        )
