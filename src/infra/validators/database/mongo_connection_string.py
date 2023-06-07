from re import match

from infra.constants._string import RegExPatternConstants
from infra.validators.base_connection_string import BaseConnectionStringValidator


class MongoConnectionStringValidator(BaseConnectionStringValidator):

    @staticmethod
    def is_valid(connection_string: str) -> bool:
        result = match(
            RegExPatternConstants.MONGO,
            string=connection_string
        )
        return bool(result)
