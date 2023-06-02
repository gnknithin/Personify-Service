import logging

import pytest
from infra.adapters.database.mongo.pymongo_adapter import PyMongoAdapter

from tests.utils.base_tests import BaseUnitTest


class TestMongoAdapter(BaseUnitTest):

    def test_should_return_an_typeerror_if_no_init_arg_is_informed(self):
        with pytest.raises(TypeError) as exec_info:
            sut = PyMongoAdapter(logger=logging.Logger)
            assert sut is None
            assert exec_info.type is TypeError
            assert exec_info.value.args[0] == str(
                "__init__() missing 1 required positional argument: 'connection_string'"
            )

    def test_should_return_an_instance_of_mongo_adapter(self):
        # Arrange
        host = 'localhost'
        username = 'fakecustomer'
        password = '123456'
        database = 'fake_database'
        driver = "mongodb"
        connection_string = f"{driver}://{username}:{password}@{host}/{database}"
        # Act
        sut = PyMongoAdapter(
            logger=logging.Logger,
            connection_string=connection_string
        )
        # Assert
        assert isinstance(sut, PyMongoAdapter)
