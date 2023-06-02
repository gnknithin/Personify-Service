from typing import Dict, List

from bootstrap import ApplicationBootstrap
from infra.generator.identity import IdentityGenerator

from tests.utils.base_tests import BaseIntegrationTest
from tests.utils.core_seed import SampleTestSeed


class TestMongoAdapter(BaseIntegrationTest):

    def test_should_check_availability_successfully(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        _mongo_adapter = init_bootstrap.mongo_adapter
        # Act
        sut = _mongo_adapter.check_availability()
        # Assert
        assert sut is True

    def _create_records(self, size: int):
        return SampleTestSeed.create_seed(size=size)

    def __sample_database_and_test_collection(self):
        return ('sample', 'adapter')

    def test_should_insert_find_update_and_delete_one_successfully(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        _db, _collection = self.__sample_database_and_test_collection()
        _seed_data = self._create_records(size=2)
        _mongo_adapter = init_bootstrap.mongo_adapter
        # Act-Insert-One
        insert_one_sut = _mongo_adapter.insert_one(
            db_name=_db,
            collection_name=_collection,
            data=_seed_data[0],
        )
        # Assert
        assert insert_one_sut is not None
        assert isinstance(insert_one_sut, str)
        # Act-Find-One
        find_one_sut = _mongo_adapter.find_one(
            db_name=_db,
            collection_name=_collection,
            key=insert_one_sut
        )
        assert find_one_sut is not None
        assert isinstance(find_one_sut, Dict)
        # Act-Find-One-And-Updae
        find_one_and_update_sut = _mongo_adapter.find_one_and_update(
            db_name=_db,
            collection_name=_collection,
            key=insert_one_sut,
            data=_seed_data[1]
        )
        assert find_one_and_update_sut is not None
        assert isinstance(find_one_and_update_sut, Dict)
        # Act-Delete-One
        delete_one_sut = _mongo_adapter.delete_one(
            db_name=_db,
            collection_name=_collection,
            key=insert_one_sut
        )
        assert delete_one_sut is not None
        assert isinstance(delete_one_sut, bool)
        assert delete_one_sut is True

    def test_should_find_one_and_return_none_successfully(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        _db, _collection = self.__sample_database_and_test_collection()
        _seed_data = self._create_records(size=1)[0]
        _mongo_adapter = init_bootstrap.mongo_adapter
        # Act-Find-One
        find_one_sut = _mongo_adapter.find_one(
            db_name=_db,
            collection_name=_collection,
            key=IdentityGenerator.get_random_id_of_object_length()
        )
        # Assert
        assert find_one_sut is None

    def test_should_delete_one_and_return_successfully(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        _db, _collection = self.__sample_database_and_test_collection()
        _seed_data = self._create_records(size=1)[0]
        _mongo_adapter = init_bootstrap.mongo_adapter
        # Act-Delete-One
        delete_one_sut = _mongo_adapter.delete_one(
            db_name=_db,
            collection_name=_collection,
            key=IdentityGenerator.get_random_id_of_object_length()
        )
        # Assert
        assert delete_one_sut is not None
        assert isinstance(delete_one_sut, bool)
        assert delete_one_sut is False

    def test_should_delete_one_and_return_none_successfully(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        _db, _collection = self.__sample_database_and_test_collection()
        _mongo_adapter = init_bootstrap.mongo_adapter
        # Act-Delete-One
        delete_one_sut = _mongo_adapter.delete_one(
            db_name=_db,
            collection_name=_collection,
            key=IdentityGenerator.get_random_id_of_object_length()
        )
        # Assert
        assert delete_one_sut is not None
        assert isinstance(delete_one_sut, bool)
        assert delete_one_sut is False

    def test_should_find_one_and_update_return_none_successfully(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        _db, _collection = self.__sample_database_and_test_collection()
        _seed_data = self._create_records(size=1)[0]
        _mongo_adapter = init_bootstrap.mongo_adapter
        # Act-Find-One-And-Update
        find_one_and_update_sut = _mongo_adapter.find_one_and_update(
            db_name=_db,
            collection_name=_collection,
            key=IdentityGenerator.get_random_id_of_object_length(),
            data=_seed_data
        )
        # Assert
        assert find_one_and_update_sut is None

    def test_should_insert_find_and_delete_many_successfully(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        _seed_size = 10
        _db, _collection = self.__sample_database_and_test_collection()
        _seed_data = self._create_records(size=_seed_size)
        _mongo_adapter = init_bootstrap.mongo_adapter
        # Act-Insert-Many
        insert_many_sut = _mongo_adapter.insert_many(
            db_name=_db,
            collection_name=_collection,
            data=_seed_data
        )
        # Assert
        assert insert_many_sut is not None
        assert isinstance(insert_many_sut, list)
        assert len(insert_many_sut) == _seed_size
        # Act-Count
        count_sut = _mongo_adapter.count(
            db_name=_db,
            collection_name=_collection
        )
        # Assert
        assert count_sut is not None
        assert isinstance(count_sut, int)
        assert count_sut == _seed_size
        # Act-Find
        find_sut = _mongo_adapter.find(
            db_name=_db,
            collection_name=_collection
        )
        # Assert
        assert find_sut is not None
        assert isinstance(find_sut, List)
        assert len(find_sut) == _seed_size
        # Act-Delete-Many
        delete_many_sut = _mongo_adapter.delete_many(
            db_name=_db,
            collection_name=_collection,
            keys=insert_many_sut
        )
        # Assert
        assert delete_many_sut is not None
        assert isinstance(delete_many_sut, bool)
        assert delete_many_sut is True
