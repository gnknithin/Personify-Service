from abc import ABC
from typing import Any, Optional


class BaseConnectionStringBuilder(ABC):
    '''
    Base connection string builder
    '''
    def __init__(
        self,
        host: Any,
        username: Optional[Any],
        password: Optional[Any],
        db_name: Optional[Any],
    ) -> None:
        self.__host = host
        self.__username = username
        self.__password = password
        self.__db_name = db_name

        super().__init__()

    @property
    def host(self) -> Any:
        """The host property."""
        return self.__host

    @property
    def username(self) -> Any:
        """The username property."""
        return self.__username

    @property
    def password(self) -> Any:
        """The password property."""
        return self.__password

    @property
    def db_name(self) -> Any:
        """The database name property."""
        return self.__db_name
