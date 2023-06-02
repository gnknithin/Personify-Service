from typing import Any, Optional
from urllib.parse import quote_plus

from infra.builders.base_connection_string import (
    BaseConnectionStringBuilder,
)
from infra.validators.full_qualified_domain_name import (
    FullQualifiedDomainNameValidator,
)


class MongoDbConnectionStringBuilder(BaseConnectionStringBuilder):

    __FULL_CONNECTION_STRING_PATTERN = "mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority&authSource=admin"
    __USER_PASSWORD_HOST_CONNECTION_STRING_PATTERN = "mongodb://{}:{}@{}/?retryWrites=true&w=majority&authSource=admin"
    __USER_HOST_CONNECTION_STRING_PATTERN = "mongodb://{}@{}/?retryWrites=true&w=majority&authSource=admin"
    __ONLY_HOST_CONNECTION_STRING_PATTERN = "mongodb://{}/?retryWrites=true&w=majority&authSource=admin"

    def __init__(
        self,
        host: Any,
        username: Optional[Any] = None,
        password: Optional[Any] = None,
        db_name: Optional[Any] = None,
    ) -> None:
        super().__init__(
            host,
            username=username,
            password=password,
            db_name=db_name
        )

        self.__encoded_username: Optional[str] = quote_plus(
            self.username) if username is not None else None
        self.__encoded_password: Optional[str] = quote_plus(
            self.password) if password is not None else None

    def get_connection_string(self) -> str:
        result = None
        if FullQualifiedDomainNameValidator.is_valid(name=self.host):
            result = self.__FULL_CONNECTION_STRING_PATTERN.format(
                self.__encoded_username,
                self.__encoded_password,
                self.host
            )
        elif self.username is not None:
            if self.password is not None:
                result = self.__USER_PASSWORD_HOST_CONNECTION_STRING_PATTERN.format(
                    self.__encoded_username,
                    self.__encoded_password,
                    self.host
                )
            else:
                result = self.__USER_HOST_CONNECTION_STRING_PATTERN.format(
                    self.__encoded_username,
                    self.host
                )
        else:
            result = self.__ONLY_HOST_CONNECTION_STRING_PATTERN.format(
                self.host)

        return result
