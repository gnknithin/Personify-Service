from re import match

from infra.constants._string import RegExPatternConstants
from infra.validators.base_connection_string import BaseConnectionStringValidator


class FullQualifiedDomainNameValidator(BaseConnectionStringValidator):

    @staticmethod
    def is_valid(name: str) -> bool:

        result = match(
            RegExPatternConstants.FQDN,
            string=name
        )

        return bool(result)
