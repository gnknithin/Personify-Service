import logging

from domain.base_model import BaseModel
from infra.adapters.database.mongo.pymongo_adapter import PyMongoAdapter
from infra.data.repositories.mongo_repository import MongoRepository

from tests.utils.base_tests import BaseUnitTest


class TestMongoRepository(BaseUnitTest):

    def _get_dummy_connection_string(self) -> str:
        host = 'localhost'
        username = 'fakeuser'
        password = '123456'
        database = 'fake_database'
        driver = "mongodb"
        return f"{driver}://{username}:{password}@{host}/{database}"

    def __sample_database_and_repository_collection(self):
        return ('sample', 'repository')

    def test_should_return_instance_of_mongo_repository(
        self
    ):
        # Arrange
        _logger = logging.Logger
        _mongo_adapter = PyMongoAdapter.from_connection_string(
            logger=_logger,
            connection_string=self._get_dummy_connection_string()
        )
        _db, _collection = self.__sample_database_and_repository_collection()
        # Act
        sut = MongoRepository(
            logger=_logger,
            db_adapter=_mongo_adapter,
            database_name=_db,
            collection_name=_collection,
            model_type=BaseModel
        )
        assert sut is not None
        assert isinstance(sut, MongoRepository)
