import json
from http import HTTPStatus
from typing import Any, Dict, List
from uuid import UUID

import pytest
from infra.constants._string import (
    FieldNameConstants,
    GenericConstants,
    HttpMethodConstants,
)
from infra.constants._url import APIEndpointV1

from tests.utils.base_tests import MainApplicationTestSetup
from tests.utils.core_seed import InitializeCoreSeed, UserSeed


class TestSignInHandlerPostMethod(MainApplicationTestSetup):

    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return UserSeed.create_seed(size=size)

    def test_post_method_raise_valueerror_successfully(self):
        # Arrange
        # Act
        with pytest.raises(ValueError) as exec_info:
            self.fetch(
                APIEndpointV1.SIGNIN_URI,
                method=HttpMethodConstants.POST,
                headers=self._get_headers(),
                body=None
            )
            # Assert
            assert exec_info.type is ValueError

    def test_post_validation_error_successfully(self):
        # Arrange
        insert_data = {'hello': 'world'}
        # Act
        response = self.fetch(
            APIEndpointV1.SIGNIN_URI,
            method=HttpMethodConstants.POST,
            headers=self._get_headers(),
            body=json.dumps(insert_data)
        )
        decoded_body = json.loads(response.body.decode(GenericConstants.UTF8))
        # Assert
        assert response.code == HTTPStatus.BAD_REQUEST
        assert response.reason == HTTPStatus.BAD_REQUEST.phrase
        assert len(decoded_body) == 2
        assert GenericConstants.SUCCESS in decoded_body
        assert isinstance(decoded_body[GenericConstants.SUCCESS], bool)
        assert decoded_body[GenericConstants.SUCCESS] is False
        assert GenericConstants.ERRORS in decoded_body
        assert isinstance(decoded_body[GenericConstants.ERRORS], list)

    def test_post_method_with_invalid_credentials_successfully(self):
        # Arrange
        _login_data: Dict[Any, Any] = dict()
        _login_data[
            FieldNameConstants.USERNAME
        ] = "dummy-username"
        _login_data[
            FieldNameConstants.PASSWORD
        ] = "dummy-password"
        # Act
        response = self.fetch(
            APIEndpointV1.SIGNIN_URI,
            method=HttpMethodConstants.POST,
            headers=self._get_headers(),
            body=json.dumps(_login_data)
        )
        decoded_body = json.loads(response.body.decode(GenericConstants.UTF8))
        # Assert
        assert response.code == HTTPStatus.BAD_REQUEST
        assert response.reason == HTTPStatus.BAD_REQUEST.phrase
        assert len(decoded_body) == 2
        assert GenericConstants.SUCCESS in decoded_body
        assert isinstance(decoded_body[GenericConstants.SUCCESS], bool)
        assert decoded_body[GenericConstants.SUCCESS] is False
        assert GenericConstants.ERRORS in decoded_body
        assert isinstance(decoded_body[GenericConstants.ERRORS], list)

    def test_post_method_successfully(self):
        # Arrange
        size = 1
        seed_data = self._create_records(size)[0]
        del seed_data[FieldNameConstants.CREATED_AT]
        del seed_data[FieldNameConstants.UPDATED_AT]
        del seed_data[FieldNameConstants.OBJECT_ID]
        seed_data[
            FieldNameConstants.DATE_OF_BIRTH
        ] = InitializeCoreSeed.get_date_isoformat()
        response = self.fetch(
            APIEndpointV1.SIGNUP_URI,
            method=HttpMethodConstants.POST,
            headers=self._get_headers(),
            body=json.dumps(seed_data, indent=4))
        assert response is not None
        assert response.code == HTTPStatus.CREATED
        assert GenericConstants.HEADER_USER_ID in response.headers
        user_id = response.headers[GenericConstants.HEADER_USER_ID]
        assert isinstance(user_id, str)
        _login_data: Dict[Any, Any] = dict()
        _login_data[
            FieldNameConstants.USERNAME
        ] = seed_data[FieldNameConstants.USERNAME]
        _login_data[
            FieldNameConstants.PASSWORD
        ] = seed_data[FieldNameConstants.PASSWORD]
        # Act
        response = self.fetch(
            APIEndpointV1.SIGNIN_URI,
            method=HttpMethodConstants.POST,
            headers=self._get_headers(),
            body=json.dumps(_login_data)
        )
        # Assert
        assert response.code == HTTPStatus.OK
        assert GenericConstants.HEADER_AUTHORIZATION in response.headers
        _authorization = response.headers[GenericConstants.HEADER_AUTHORIZATION]
        assert _authorization is not None
        assert isinstance(_authorization, str)
        # Clean-Up
        user_service = self.get_user_service()
        result = user_service.deleteUser(user_id=UUID(user_id))
        assert result is True

    def test_post_method_with_invalid_password_successfully(self):
        # Arrange
        size = 1
        seed_data = self._create_records(size)[0]
        del seed_data[FieldNameConstants.CREATED_AT]
        del seed_data[FieldNameConstants.UPDATED_AT]
        del seed_data[FieldNameConstants.OBJECT_ID]
        seed_data[
            FieldNameConstants.DATE_OF_BIRTH
        ] = InitializeCoreSeed.get_date_isoformat()
        response = self.fetch(
            APIEndpointV1.SIGNUP_URI,
            method=HttpMethodConstants.POST,
            headers=self._get_headers(),
            body=json.dumps(seed_data, indent=4))
        assert response is not None
        assert response.code == HTTPStatus.CREATED
        assert GenericConstants.HEADER_USER_ID in response.headers
        user_id = response.headers[GenericConstants.HEADER_USER_ID]
        assert isinstance(user_id, str)
        _login_data: Dict[Any, Any] = dict()
        _login_data[
            FieldNameConstants.USERNAME
        ] = seed_data[FieldNameConstants.USERNAME]
        _login_data[
            FieldNameConstants.PASSWORD
        ] = "wrong-password"
        # Act
        response = self.fetch(
            APIEndpointV1.SIGNIN_URI,
            method=HttpMethodConstants.POST,
            headers=self._get_headers(),
            body=json.dumps(_login_data)
        )
        decoded_body = json.loads(response.body.decode(GenericConstants.UTF8))
        # Assert
        assert response.code == HTTPStatus.BAD_REQUEST
        assert response.reason == HTTPStatus.BAD_REQUEST.phrase
        assert len(decoded_body) == 2
        assert GenericConstants.SUCCESS in decoded_body
        assert isinstance(decoded_body[GenericConstants.SUCCESS], bool)
        assert decoded_body[GenericConstants.SUCCESS] is False
        assert GenericConstants.ERRORS in decoded_body
        assert isinstance(decoded_body[GenericConstants.ERRORS], list)
        # Clean-Up
        user_service = self.get_user_service()
        result = user_service.deleteUser(user_id=UUID(user_id))
        assert result is True
