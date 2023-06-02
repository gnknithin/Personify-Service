from re import match

from infra.constants._string import RegExPatternConstants


class MongoConnectionStringValidator():

    @staticmethod
    def is_valid(connection_string: str) -> bool:
        result = match(
            RegExPatternConstants.MONGO,
            string=connection_string
        )
        return bool(result)
