from re import match
from typing import Optional

from infra.constants._string import RegExPatternConstants


class AuthenticationBearerTokenParser():

    @staticmethod
    def extract(value: str) -> Optional[str]:
        g = match(RegExPatternConstants.BEARER, value)
        _token: Optional[str] = None
        if g:
            _token = g.group(1)
        return _token
