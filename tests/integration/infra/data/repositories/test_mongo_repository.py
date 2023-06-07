from typing import Any, Dict, List

from bootstrap import ApplicationBootstrap
from domain.base_model import BaseModel
from infra.constants._string import FieldNameConstants
from infra.data.repositories.mongo_repository import MongoRepository
from infra.generator.identity import IdentityGenerator

from tests.utils.base_tests import BaseIntegrationTest
from tests.utils.core_seed import BaseSeed


class TestMongoRepository(BaseIntegrationTest):

    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return BaseSeed.create_seed(size=size)

    def __sample_database_and_repository_collection(self):
        return ('sample', 'repository')

    def __get_mongo_repository(
        self,
        init_bootstrap: ApplicationBootstrap
    ) -> MongoRepository[BaseModel]:
        _logger = init_bootstrap.logger
        _mongo_adapter = init_bootstrap.mongo_adapter
        _db, _collection = self.__sample_database_and_repository_collection()
        return MongoRepository[BaseModel](
            logger=_logger,
            db_adapter=_mongo_adapter,
            database_name=_db,
            collection_name=_collection,
            model_type=BaseModel
        )

    def test_should_return_instance_of_mongo_repository(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        _logger = init_bootstrap.logger
        _mongo_adapter = init_bootstrap.mongo_adapter
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

    def test_should_add_and_get_and_by_key_and_update_and_remove_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        _mongo_repository = self.__get_mongo_repository(
            init_bootstrap=init_bootstrap
        )
        seed_base_model = BaseModel().load(data=dict())
        # Act-Add
        _sut_add = _mongo_repository.add(data=seed_base_model)
        # Assert
        assert _sut_add is not None
        assert isinstance(_sut_add, str)
        # Act-Get
        _sut_get = _mongo_repository.get()
        assert _sut_get is not None
        assert isinstance(_sut_get, List)
        # Act-Get-By-Key
        _sut_get_by_key = _mongo_repository.get_by_key(
            key=_sut_add
        )
        assert _sut_get_by_key is not None
        assert isinstance(_sut_get_by_key, Dict)

        # Act-Update
        update_seed_data = self._create_records(size=1)[0]
        update_seed_data[
            FieldNameConstants.OBJECT_ID
        ] = _sut_add
        update_base_model = BaseModel().load(
            data=update_seed_data
        )
        _sut_update = _mongo_repository.update(
            key=_sut_add,
            data=update_base_model
        )
        assert _sut_update is not None
        assert isinstance(_sut_update, Dict)
        # Clean-Up
        assert _mongo_repository.remove(key=_sut_add) is True

    def test_get_by_key_should_return_none_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        _mongo_repository = self.__get_mongo_repository(
            init_bootstrap=init_bootstrap
        )
        # Act
        sut = _mongo_repository.get_by_key(
            key=IdentityGenerator.get_random_id_of_object_length()
        )
        # Assert
        assert sut is None

    def test_remove_should_return_none_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        _mongo_repository = self.__get_mongo_repository(
            init_bootstrap=init_bootstrap
        )
        # Act
        sut = _mongo_repository.remove(
            key=IdentityGenerator.get_random_id_of_object_length()
        )
        # Assert
        assert sut is not None
        assert isinstance(sut, bool)
        assert sut is False

    def test_update_should_return_none_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        _mongo_repository = self.__get_mongo_repository(
            init_bootstrap=init_bootstrap
        )
        # Act
        sut = _mongo_repository.update(
            key=IdentityGenerator.get_random_id_of_object_length(),
            data=dict()
        )
        # Assert
        assert sut is None

    def test_get_should_return_list_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        _mongo_repository = self.__get_mongo_repository(
            init_bootstrap=init_bootstrap
        )
        # Act
        sut = _mongo_repository.get()
        # Assert
        assert sut is not None
        assert isinstance(sut, List)
