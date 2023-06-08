from datetime import date
from typing import Any, Dict, List

import pytest
from domain.user_model import UserModel
from infra.constants._string import FieldNameConstants
from interfaces.http.tornado.schemas.v1.user_schema import SignUpSchema
from marshmallow.exceptions import ValidationError

from tests.utils.base_tests import BaseUnitTest
from tests.utils.core_seed import InitializeCoreSeed, UserSeed


class TestSignUpSchema(BaseUnitTest):

    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return UserSeed.create_seed(size=size)

    def test_should_return_an_instance_properly(self):
        # Arrange
        # Act
        sut = SignUpSchema()
        # Assert
        assert sut is not None
        assert isinstance(sut, SignUpSchema)

    def test_should_raise_validation_error(self):
        with pytest.raises(ValidationError) as validation_err:
            # Arrange
            # Act
            SignUpSchema().load(data=dict())
            # Assert
            assert validation_err.type is ValidationError

    def test_should_load_and_return_properly(self):
        # Arrange
        size = 1
        seed_data = self._create_records(size)[0]
        del seed_data[FieldNameConstants.CREATED_AT]
        del seed_data[FieldNameConstants.UPDATED_AT]
        del seed_data[FieldNameConstants.OBJECT_ID]
        seed_data[
            FieldNameConstants.DATE_OF_BIRTH
        ] = InitializeCoreSeed.get_date_isoformat()
        # Act
        sut = SignUpSchema().load(data=seed_data)
        # Assert
        assert sut is not None
        assert isinstance(sut, UserModel)
        assert hasattr(sut, FieldNameConstants.CREATED_AT)
        assert hasattr(sut, FieldNameConstants.UPDATED_AT)
        assert hasattr(sut, FieldNameConstants.OBJECT_ID)
        assert hasattr(sut, FieldNameConstants.USERNAME)
        assert hasattr(sut, FieldNameConstants.PASSWORD)
        assert hasattr(sut, FieldNameConstants.FULL_NAME)
        assert hasattr(sut, FieldNameConstants.DATE_OF_BIRTH)
        assert hasattr(sut, FieldNameConstants.EMAIL)
        assert sut.created_at is None
        assert sut.updated_at is None
        assert sut._id is None
        assert isinstance(sut.username, str)
        assert isinstance(sut.password, str)
        assert isinstance(sut.full_name, str)
        assert isinstance(sut.date_of_birth, date)
        assert isinstance(sut.email, str)

    def test_should_load_only_required_and_return_properly(self):
        # Arrange
        size = 1
        seed_data = self._create_records(size)[0]
        del seed_data[FieldNameConstants.CREATED_AT]
        del seed_data[FieldNameConstants.UPDATED_AT]
        del seed_data[FieldNameConstants.OBJECT_ID]
        del seed_data[FieldNameConstants.EMAIL]
        seed_data[
            FieldNameConstants.DATE_OF_BIRTH
        ] = InitializeCoreSeed.get_date_isoformat()
        # Act
        sut = SignUpSchema().load(data=seed_data)
        # Assert
        assert sut is not None
        assert isinstance(sut, UserModel)
        assert hasattr(sut, FieldNameConstants.CREATED_AT)
        assert hasattr(sut, FieldNameConstants.UPDATED_AT)
        assert hasattr(sut, FieldNameConstants.OBJECT_ID)
        assert hasattr(sut, FieldNameConstants.USERNAME)
        assert hasattr(sut, FieldNameConstants.PASSWORD)
        assert hasattr(sut, FieldNameConstants.FULL_NAME)
        assert hasattr(sut, FieldNameConstants.DATE_OF_BIRTH)
        assert hasattr(sut, FieldNameConstants.EMAIL)
        assert sut.created_at is None
        assert sut.updated_at is None
        assert sut._id is None
        assert isinstance(sut.username, str)
        assert isinstance(sut.password, str)
        assert isinstance(sut.full_name, str)
        assert isinstance(sut.date_of_birth, date)
        assert sut.email is None
