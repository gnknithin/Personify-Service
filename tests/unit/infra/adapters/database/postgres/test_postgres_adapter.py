import logging

import pytest
from infra.adapters.database.postgres.postgres_adapter import PostgresAdapter

from tests.utils.base_tests import BaseUnitTest


class TestPostgresAdapter(BaseUnitTest):

    def test_should_return_an_typeerror_if_no_init_arg_is_informed(self):
        with pytest.raises(TypeError) as exec_info:
            sut = PostgresAdapter(logger=logging.Logger)
            assert sut is None
            assert exec_info.type is TypeError
            assert exec_info.value.args[0] == str(
                "__init__() missing 1 required positional argument: 'connection_string'"
            )

    def _get_dummy_connection_string(self) -> str:
        host = 'localhost'
        username = 'fakecustomer'
        password = '123456'
        database = 'fake_database'
        driver = "postgresql+psycopg2"
        return f"{driver}://{username}:{password}@{host}/{database}"

    def test_should_return_an_instance_of_postgres_adapter(self):
        # Arrange
        # Act
        sut = PostgresAdapter(
            logger=logging.Logger,
            connection_string=self._get_dummy_connection_string()
        )
        # Assert
        assert isinstance(sut, PostgresAdapter)
