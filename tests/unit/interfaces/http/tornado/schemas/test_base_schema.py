
from typing import Any, Dict, List

import pytest
from infra.constants._string import GenericConstants
from interfaces.http.tornado.schemas.base_schema import (
    BadRequestSchema,
    BaseErrorSchema,
    BaseSuccessSchema,
    NotFoundSchema,
    ServerErrorSchema,
)
from marshmallow.exceptions import ValidationError

from tests.utils.base_tests import BaseUnitTest
from tests.utils.core_seed import BadRequestSchemaSeed, BaseSuccessSchemaSeed


class TestBaseSuccessSchema(BaseUnitTest):

    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return BaseSuccessSchemaSeed.create_seed(size=size)

    def test_should_return_a_validation_error_with_properly(self):
        with pytest.raises(ValidationError) as validation_err:
            # Arrange
            seed_data: Dict[Any, Any] = dict()
            seed_data[GenericConstants.SUCCESS] = None
            # Act
            BaseSuccessSchema().load(data=seed_data)
            # Assert
            assert validation_err.type is ValidationError

    def test_should_return_an_instance_of_basesuccessschema_properly(self):
        # Arrange
        # Act
        sut = BaseSuccessSchema()
        # Assert
        assert sut is not None
        assert isinstance(sut, BaseSuccessSchema)

    def test_should_load_and_return_an_instance_properly(self):
        # Arrange
        seed_data: Dict[Any, Any] = self._create_records(size=1)[0]
        # Act
        sut = BaseSuccessSchema().load(data=seed_data)
        # Assert
        assert sut is not None
        assert isinstance(sut, Dict)
        assert GenericConstants.SUCCESS in sut
        assert isinstance(sut[GenericConstants.SUCCESS], bool)


class TestBaseErrorSchema(BaseUnitTest):

    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return BaseSuccessSchemaSeed.create_seed(size=size)

    def test_should_return_a_validation_error_with_properly(self):
        with pytest.raises(ValidationError) as validation_err:
            # Arrange
            seed_data: Dict[Any, Any] = dict()
            seed_data[GenericConstants.SUCCESS] = None
            # Act
            BaseErrorSchema().load(data=seed_data)
            # Assert
            assert validation_err.type is ValidationError

    def test_should_return_an_instance_of_baseerrorschema_properly(self):
        # Arrange
        # Act
        sut = BaseErrorSchema()
        # Assert
        assert sut is not None
        assert isinstance(sut, BaseErrorSchema)

    def test_should_load_and_return_an_instance_properly(self):
        # Arrange
        seed_data: Dict[Any, Any] = self._create_records(size=1)[0]
        # Act
        sut = BaseErrorSchema().load(data=seed_data)
        # Assert
        assert sut is not None
        assert isinstance(sut, Dict)
        assert GenericConstants.SUCCESS in sut
        assert isinstance(sut[GenericConstants.SUCCESS], bool)


class TestBadRequestSchema(BaseUnitTest):

    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return BadRequestSchemaSeed.create_seed(size=size)

    def test_should_return_a_validation_error_with_properly(self):
        with pytest.raises(ValidationError) as validation_err:
            # Arrange
            seed_data: Dict[Any, Any] = dict()
            seed_data[GenericConstants.SUCCESS] = None
            seed_data[GenericConstants.ERRORS] = None
            # Act
            BadRequestSchema().load(data=seed_data)
            # Assert
            assert validation_err.type is ValidationError

    def test_should_return_an_instance_of_badrequestschema_properly(self):
        # Arrange
        # Act
        sut = BadRequestSchema()
        # Assert
        assert sut is not None
        assert isinstance(sut, BadRequestSchema)

    def test_should_load_and_return_an_instance_properly(self):
        # Arrange
        seed_data = self._create_records(size=1)[0]
        # Act
        sut = BadRequestSchema().load(data=seed_data)
        # Assert
        assert sut is not None
        assert GenericConstants.SUCCESS in sut
        assert isinstance(sut[GenericConstants.SUCCESS], bool)
        assert GenericConstants.ERRORS in sut
        assert isinstance(sut[GenericConstants.ERRORS], list)
        for item in sut[GenericConstants.ERRORS]:
            assert item is not None
            assert isinstance(item, str)


class TestNotFoundSchema(BaseUnitTest):

    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return BadRequestSchemaSeed.create_seed(size=size)

    def test_should_return_a_validation_error_with_properly(self):
        with pytest.raises(ValidationError) as validation_err:
            # Arrange
            seed_data: Dict[Any, Any] = dict()
            seed_data[GenericConstants.SUCCESS] = None
            seed_data[GenericConstants.ERRORS] = None
            # Act
            NotFoundSchema().load(data=seed_data)
            # Assert
            assert validation_err.type is ValidationError

    def test_should_return_an_instance_of_notfoundschema_properly(self):
        # Arrange
        # Act
        sut = NotFoundSchema()
        # Assert
        assert sut is not None
        assert isinstance(sut, NotFoundSchema)

    def test_should_load_and_return_an_instance_properly(self):
        # Arrange
        seed_data: Dict[Any, Any] = self._create_records(size=1)[0]
        # Act
        sut = NotFoundSchema().load(data=seed_data)
        # Assert
        assert sut is not None
        assert GenericConstants.SUCCESS in sut
        assert isinstance(sut[GenericConstants.SUCCESS], bool)
        assert GenericConstants.ERRORS in sut
        assert isinstance(sut[GenericConstants.ERRORS], list)
        for item in sut[GenericConstants.ERRORS]:
            assert item is not None
            assert isinstance(item, str)


class TestServerErrorSchema(BaseUnitTest):

    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return BadRequestSchemaSeed.create_seed(size=size)

    def test_should_return_a_validation_error_with_properly(self):
        with pytest.raises(ValidationError) as validation_err:
            # Arrange
            seed_data: Dict[Any, Any] = dict()
            seed_data[GenericConstants.SUCCESS] = None
            seed_data[GenericConstants.ERRORS] = None
            # Act
            ServerErrorSchema().load(data=seed_data)
            # Assert
            assert validation_err.type is ValidationError

    def test_should_return_an_instance_of_servererrorschema_properly(self):
        # Arrange
        # Act
        sut = ServerErrorSchema()
        # Assert
        assert sut is not None
        assert isinstance(sut, ServerErrorSchema)

    def test_should_load_and_return_an_instance_properly(self):
        # Arrange
        seed_data: Dict[Any, Any] = self._create_records(size=1)[0]
        # Act
        sut = ServerErrorSchema().load(data=seed_data)
        # Assert
        assert sut is not None
        assert GenericConstants.SUCCESS in sut
        assert isinstance(sut[GenericConstants.SUCCESS], bool)
        assert GenericConstants.ERRORS in sut
        assert isinstance(sut[GenericConstants.ERRORS], list)
        for item in sut[GenericConstants.ERRORS]:
            assert item is not None
            assert isinstance(item, str)
