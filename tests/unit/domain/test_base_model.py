from datetime import datetime
from typing import Any, Dict, List

from domain.base_model import BaseModel
from infra.constants._string import FieldNameConstants

from tests.utils.base_tests import BaseUnitTest
from tests.utils.core_seed import BaseIdSeed


class TestBaseModel(BaseUnitTest):
    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return BaseIdSeed.create_seed(size=size)

    def test_should_load_empty(self):
        # Arrange
        seed_data: Dict[Any, Any] = dict()
        # Act
        sut = BaseModel().load(data=seed_data)
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)
        assert len(sut) == 0

    def test_should_dump_empty(self):
        # Arrange
        seed_data: Dict[Any, Any] = dict()
        loaded_data: Dict[Any, Any] = BaseModel().load(data=seed_data)
        # Act
        sut = BaseModel().dump(obj=loaded_data)
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)
        assert FieldNameConstants.CREATED_AT in sut
        assert isinstance(sut[FieldNameConstants.CREATED_AT], str)
        assert FieldNameConstants.UPDATED_AT in sut
        assert isinstance(sut[FieldNameConstants.UPDATED_AT], str)

    def test_should_load_and_return_successfuly(self):
        # Arrange
        seed_data: Dict[Any, Any] = self._create_records(size=1)[0]
        # Act
        sut = BaseModel().load(data=seed_data)
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)
        assert FieldNameConstants.OBJECT_ID in sut
        assert isinstance(sut[FieldNameConstants.OBJECT_ID], str)
        assert FieldNameConstants.CREATED_AT in sut
        assert isinstance(sut[FieldNameConstants.CREATED_AT], datetime)
        assert FieldNameConstants.UPDATED_AT in sut
        assert isinstance(sut[FieldNameConstants.UPDATED_AT], datetime)

    def test_should_dump_and_return_successfuly(self):
        # Arrange
        seed_data: Dict[Any, Any] = self._create_records(size=1)[0]
        loaded_data: Dict[Any, Any] = BaseModel().load(data=seed_data)
        # Act
        sut = BaseModel().dump(obj=loaded_data)
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)
        assert FieldNameConstants.CREATED_AT in sut
        assert isinstance(sut[FieldNameConstants.CREATED_AT], str)
        assert FieldNameConstants.UPDATED_AT in sut
        assert isinstance(sut[FieldNameConstants.UPDATED_AT], str)
