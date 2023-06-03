from datetime import date, datetime
from typing import Any, Dict, List
from uuid import UUID

import pytest
from domain.contact_model import ContactModel
from infra.constants._string import FieldNameConstants
from marshmallow import ValidationError

from tests.utils.base_tests import BaseUnitTest
from tests.utils.core_seed import ContactSeed


class TestBaseModel(BaseUnitTest):
    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return ContactSeed.create_seed(size=size)

    def test_should_raise_validation_error(self):
        with pytest.raises(ValidationError) as validation_error:
            # Arrange
            seed_data: Dict[Any, Any] = dict()
            # Act
            sut = ContactModel().load(data=seed_data)
            # Assert
            assert validation_error.type is ValidationError

    def test_should_load_return_an_instance_properly(self):
        # Arrange
        seed_data: Dict[Any, Any] = self._create_records(size=1)[0]
        # Act
        sut = ContactModel().load(data=seed_data)
        # Assert
        assert sut is not None
        assert isinstance(sut, Dict)
        assert len(sut) == 9
        assert FieldNameConstants.EMAIL in sut
        assert isinstance(sut[FieldNameConstants.EMAIL], str)
        assert FieldNameConstants.USER_ID in sut
        assert isinstance(sut[FieldNameConstants.USER_ID], UUID)
        assert FieldNameConstants.BIRTHDAY in sut
        assert isinstance(sut[FieldNameConstants.BIRTHDAY], date)
        assert FieldNameConstants.MOBILE in sut
        assert isinstance(sut[FieldNameConstants.MOBILE], str)
        assert FieldNameConstants.OBJECT_ID in sut
        assert isinstance(sut[FieldNameConstants.OBJECT_ID], str)
        assert FieldNameConstants.UPDATED_AT in sut
        assert isinstance(sut[FieldNameConstants.UPDATED_AT], datetime)
        assert FieldNameConstants.CREATED_AT in sut
        assert isinstance(sut[FieldNameConstants.CREATED_AT], datetime)
        assert FieldNameConstants.FULL_NAME in sut
        assert isinstance(sut[FieldNameConstants.FULL_NAME], str)
        assert FieldNameConstants.CONTACT_ID in sut
        assert isinstance(sut[FieldNameConstants.CONTACT_ID], str)

    def test_should_load_only_required_true_and_return_an_instance_properly(self):
        # Arrange
        seed_data: Dict[Any, Any] = self._create_records(size=1)[0]
        del seed_data[FieldNameConstants.EMAIL]
        del seed_data[FieldNameConstants.BIRTHDAY]
        del seed_data[FieldNameConstants.MOBILE]
        del seed_data[FieldNameConstants.OBJECT_ID]
        del seed_data[FieldNameConstants.UPDATED_AT]
        del seed_data[FieldNameConstants.CREATED_AT]
        # Act
        sut = ContactModel().load(data=seed_data)
        # Assert
        assert sut is not None
        assert isinstance(sut, Dict)
        assert FieldNameConstants.EMAIL not in sut
        assert FieldNameConstants.USER_ID in sut
        assert isinstance(sut[FieldNameConstants.USER_ID], UUID)
        assert FieldNameConstants.BIRTHDAY not in sut
        assert FieldNameConstants.MOBILE not in sut
        assert FieldNameConstants.OBJECT_ID not in sut
        assert FieldNameConstants.UPDATED_AT not in sut
        assert FieldNameConstants.CREATED_AT not in sut
        assert FieldNameConstants.FULL_NAME in sut
        assert isinstance(sut[FieldNameConstants.FULL_NAME], str)

    def test_should_load_only_required_with_object_id_properly(self):
        # Arrange
        seed_data: Dict[Any, Any] = self._create_records(size=1)[0]
        del seed_data[FieldNameConstants.EMAIL]
        del seed_data[FieldNameConstants.BIRTHDAY]
        del seed_data[FieldNameConstants.MOBILE]
        del seed_data[FieldNameConstants.UPDATED_AT]
        del seed_data[FieldNameConstants.CREATED_AT]
        # Act
        sut = ContactModel().load(data=seed_data)
        # Assert
        assert sut is not None
        assert isinstance(sut, Dict)
        assert len(sut) == 4
        assert FieldNameConstants.EMAIL not in sut
        assert FieldNameConstants.USER_ID in sut
        assert isinstance(sut[FieldNameConstants.USER_ID], UUID)
        assert FieldNameConstants.BIRTHDAY not in sut
        assert FieldNameConstants.MOBILE not in sut
        assert FieldNameConstants.OBJECT_ID in sut
        assert isinstance(sut[FieldNameConstants.OBJECT_ID], str)
        assert FieldNameConstants.UPDATED_AT not in sut
        assert FieldNameConstants.CREATED_AT not in sut
        assert FieldNameConstants.FULL_NAME in sut
        assert isinstance(sut[FieldNameConstants.FULL_NAME], str)
        assert FieldNameConstants.CONTACT_ID in sut
        assert isinstance(sut[FieldNameConstants.CONTACT_ID], str)

    def test_should_load_and_dump_an_instance_properly(self):
        # Arrange
        seed_data: Dict[Any, Any] = self._create_records(size=1)[0]
        loaded_model = ContactModel().load(data=seed_data)
        # Act
        sut = ContactModel().dump(obj=loaded_model)
        # Assert
        assert sut is not None
        assert isinstance(sut, Dict)
        assert FieldNameConstants.EMAIL in sut
        assert isinstance(sut[FieldNameConstants.EMAIL], str)
        assert FieldNameConstants.USER_ID in sut
        assert isinstance(sut[FieldNameConstants.USER_ID], str)
        assert FieldNameConstants.BIRTHDAY in sut
        assert isinstance(sut[FieldNameConstants.BIRTHDAY], str)
        assert FieldNameConstants.MOBILE in sut
        assert isinstance(sut[FieldNameConstants.MOBILE], str)
        assert FieldNameConstants.OBJECT_ID not in sut
        assert FieldNameConstants.UPDATED_AT in sut
        assert isinstance(sut[FieldNameConstants.UPDATED_AT], str)
        assert FieldNameConstants.CREATED_AT in sut
        assert isinstance(sut[FieldNameConstants.CREATED_AT], str)
        assert FieldNameConstants.FULL_NAME in sut
        assert isinstance(sut[FieldNameConstants.FULL_NAME], str)

    def test_should_load_only_required_true_and_dump_properly(self):
        # Arrange
        seed_data: Dict[Any, Any] = self._create_records(size=1)[0]
        del seed_data[FieldNameConstants.EMAIL]
        del seed_data[FieldNameConstants.BIRTHDAY]
        del seed_data[FieldNameConstants.MOBILE]
        del seed_data[FieldNameConstants.OBJECT_ID]
        del seed_data[FieldNameConstants.UPDATED_AT]
        del seed_data[FieldNameConstants.CREATED_AT]
        loaded_model = ContactModel().load(data=seed_data)
        # Act
        sut = ContactModel().dump(obj=loaded_model)
        # Assert
        assert sut is not None
        assert isinstance(sut, Dict)
        assert FieldNameConstants.EMAIL not in sut
        assert FieldNameConstants.USER_ID in sut
        assert isinstance(sut[FieldNameConstants.USER_ID], str)
        assert FieldNameConstants.BIRTHDAY not in sut
        assert FieldNameConstants.MOBILE not in sut
        assert FieldNameConstants.OBJECT_ID not in sut
        assert FieldNameConstants.UPDATED_AT not in sut
        assert FieldNameConstants.CREATED_AT not in sut
        assert FieldNameConstants.FULL_NAME in sut
        assert isinstance(sut[FieldNameConstants.FULL_NAME], str)
