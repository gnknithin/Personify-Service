from datetime import date, datetime
from typing import Any, Dict, List
from uuid import UUID

from domain.user_model import UserModel
from infra.constants._string import FieldNameConstants

from tests.utils.base_tests import BaseUnitTest
from tests.utils.core_seed import UserSeed


class TestUserModel(BaseUnitTest):
    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return UserSeed.create_seed(size=size)

    def test_should_return_a_model_instance_properly(self):
        # Arrange
        seed_user_data = self._create_records(size=1)[0]
        # Act
        sut = UserModel(**seed_user_data)
        # Assert
        assert isinstance(sut, UserModel)
        assert hasattr(sut, FieldNameConstants.CREATED_AT)
        assert hasattr(sut, FieldNameConstants.UPDATED_AT)
        assert hasattr(sut, FieldNameConstants.OBJECT_ID)
        assert hasattr(sut, FieldNameConstants.USERNAME)
        assert hasattr(sut, FieldNameConstants.PASSWORD)
        assert hasattr(sut, FieldNameConstants.FULL_NAME)
        assert hasattr(sut, FieldNameConstants.DATE_OF_BIRTH)
        assert hasattr(sut, FieldNameConstants.EMAIL)
        assert isinstance(sut.created_at, datetime)
        assert isinstance(sut.updated_at, datetime)
        assert isinstance(sut._id, UUID)
        assert isinstance(sut.username, str)
        assert isinstance(sut.password, str)
        assert isinstance(sut.full_name, str)
        assert isinstance(sut.date_of_birth, date)
        assert isinstance(sut.email, str)
