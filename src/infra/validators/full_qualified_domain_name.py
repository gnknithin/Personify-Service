from re import match

from infra.constants._string import RegExPatternConstants


class FullQualifiedDomainNameValidator():

    @staticmethod
    def is_valid(name: str) -> bool:

        result = match(
            RegExPatternConstants.FQDN,
            string=name
        )

        return bool(result)
