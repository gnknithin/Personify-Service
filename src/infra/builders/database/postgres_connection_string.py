from typing import Any, Optional
from urllib.parse import quote_plus

from infra.builders.base_connection_string import BaseConnectionStringBuilder
from infra.validators.full_qualified_domain_name import FullQualifiedDomainNameValidator


class PostgresConnectionStringBuilder(BaseConnectionStringBuilder):

    __FULL_CONNECTION_STRING_PATTERN = "postgresql+psycopg2://{}:{}@{}/{}"
    __USER_PASSWORD_HOST_CONNECTION_STRING_PATTERN = "postgresql+psycopg2://{}:{}@{}/{}"
    __USER_HOST_CONNECTION_STRING_PATTERN = "postgresql+psycopg2://{}@{}/{}"
    __ONLY_HOST_CONNECTION_STRING_PATTERN = "postgresql+psycopg2://{}/{}"

    def __init__(
        self,
        host: Any,
        username: Optional[Any],
        password: Optional[Any],
        database_name: Optional[Any]
    ):
        super().__init__(
            host,
            username=username,
            password=password,
            database_name=database_name
        )

        self.__encoded_username = quote_plus(
            self.username) if username is not None else None
        self.__encoded_password = quote_plus(
            self.password) if password is not None else None

    def get_connection_string(self) -> str:
        result = None

        if FullQualifiedDomainNameValidator.is_valid(self.host):
            result = self.__FULL_CONNECTION_STRING_PATTERN.format(
                self.__encoded_username,
                self.__encoded_password,
                self.host,
                self.db_name
            )
        elif self.username is not None:
            if self.password is not None:
                result = self.__USER_PASSWORD_HOST_CONNECTION_STRING_PATTERN.format(
                    self.__encoded_username,
                    self.__encoded_password,
                    self.host,
                    self.db_name
                )
            else:
                result = self.__USER_HOST_CONNECTION_STRING_PATTERN.format(
                    self.__encoded_username,
                    self.host,
                    self.db_name
                )
        else:
            result = self.__ONLY_HOST_CONNECTION_STRING_PATTERN.format(
                self.host,
                self.db_name
            )

        return result
