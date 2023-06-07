import logging
from typing import Any, Dict

from infra.adapters.database.base_database_adapter import BaseDatabaseAdapter
from infra.builders.database.postgres_connection_string import (
    PostgresConnectionStringBuilder,
)
from infra.validators.database.postgres_connection_string import (
    PostgresConnectionStringValidator,
)
from sqlalchemy import create_engine


class PostgresAdapter(BaseDatabaseAdapter):

    def __init__(
        self,
        logger: logging.Logger,
        connection_string: str
    ) -> None:
        super().__init__(logger=logger)
        if not PostgresConnectionStringValidator.is_valid(
            connection_string=connection_string
        ):
            raise ValueError

        self._connection_string = connection_string

        self._engine = create_engine(
            self._connection_string,
            echo=True
        )

    @classmethod
    def from_connection_string(
        cls,
        logger: logging.Logger,
        connection_string: str
    ) -> 'PostgresAdapter':
        return cls(logger=logger, connection_string=connection_string)

    @classmethod
    def from_dict(
        cls,
        logger: logging.Logger,
        **connection_info: Dict[Any, Any]
    ) -> 'PostgresAdapter':
        return cls(
            logger=logger,
            connection_string=PostgresConnectionStringBuilder(
                **connection_info).get_connection_string()
        )

    @property
    def engine(self):
        """The engine property"""
        return self._engine

    def check_availability(self) -> bool:
        result = False
        with self.engine.connect() as connection:
            result = not connection.closed
        return result
