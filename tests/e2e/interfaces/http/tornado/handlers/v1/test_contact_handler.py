import json
from http import HTTPStatus
from typing import Any, Dict, List
from uuid import UUID

from domain.user_model import UserModel
from infra.constants._string import (
    FieldNameConstants,
    GenericConstants,
    HttpMethodConstants,
)
from infra.constants._url import APIEndpointV1

from tests.utils.base_tests import MainApplicationTestSetup
from tests.utils.core_seed import ContactSeed, UserSeed


class TestContactHandlerPostMethod(MainApplicationTestSetup):

    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return ContactSeed.create_seed(size=size)

    def _create_user_records(self, size: int) -> List[Dict[Any, Any]]:
        return UserSeed.create_seed(size=size)

    def test_should_raise_unauthorized_error_successfully(self):
        # Arrange
        insert_data = {'hello': 'world'}
        _body = json.dumps(insert_data)
        _headers = self._get_headers()
        # Act
        response = self.fetch(
            APIEndpointV1.CONTACT_URI,
            method=HttpMethodConstants.POST,
            headers=_headers,
            body=_body
        )
        # Assert
        assert response.code == HTTPStatus.UNAUTHORIZED
        assert response.reason == HTTPStatus.UNAUTHORIZED.phrase
        # Arrange
        _headers[GenericConstants.HEADER_AUTHORIZATION] = "hello"
        # Act
        response = self.fetch(
            APIEndpointV1.CONTACT_URI,
            method=HttpMethodConstants.POST,
            headers=_headers,
            body=_body
        )
        # Assert
        assert response.code == HTTPStatus.UNAUTHORIZED
        assert response.reason == HTTPStatus.UNAUTHORIZED.phrase
        # Arrange
        _headers[
            GenericConstants.HEADER_AUTHORIZATION
        ] = "Bearer Says-Hello-Authentication"
        # Act
        response = self.fetch(
            APIEndpointV1.CONTACT_URI,
            method=HttpMethodConstants.POST,
            headers=_headers,
            body=_body
        )
        # Assert
        assert response.code == HTTPStatus.UNAUTHORIZED
        assert response.reason == HTTPStatus.UNAUTHORIZED.phrase
        # Arrange
        # ruff: noqa: E501
        _headers[
            GenericConstants.HEADER_AUTHORIZATION
        ] = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJoZWxsbyI6IndvcmxkIn0.4Cwa6iEaaQcfcsSdUf1PzCP24RPOz7rGaVd5rNhvszI"
        # Act
        response = self.fetch(
            APIEndpointV1.CONTACT_URI,
            method=HttpMethodConstants.POST,
            headers=_headers,
            body=_body
        )
        # Assert
        assert response.code == HTTPStatus.UNAUTHORIZED
        assert response.reason == HTTPStatus.UNAUTHORIZED.phrase

    def test_post_method_successfully(self):
        # Arrange-User
        user_service = self.get_user_service()
        seed_user_data = self._create_user_records(size=1)[0]
        del seed_user_data[FieldNameConstants.CREATED_AT]
        del seed_user_data[FieldNameConstants.UPDATED_AT]
        del seed_user_data[FieldNameConstants.OBJECT_ID]
        _user_model = UserModel(**seed_user_data)
        user_id = user_service.createUser(data=_user_model)
        assert user_id is not None
        assert isinstance(user_id, UUID)
        # Arrange-Bearer-Token
        _login: Dict[Any, Any] = dict()
        _login[
            FieldNameConstants.USERNAME
        ] = seed_user_data[FieldNameConstants.USERNAME]
        _login[
            FieldNameConstants.PASSWORD
        ] = seed_user_data[FieldNameConstants.PASSWORD]
        _login_user = UserModel(**_login)
        _token = user_service.loginUserWithCredentials(data=_login_user)
        assert _token is not None
        assert isinstance(_token, str)
        # Arrange-Headers
        _headers = self._get_headers()
        _headers[
            GenericConstants.HEADER_AUTHORIZATION
        ] = f'Bearer {_token}'
        # Arrange-Insert-Contact-Data
        insert_data = self._create_records(size=1)[0]
        del insert_data[FieldNameConstants.OBJECT_ID]
        del insert_data[FieldNameConstants.USER_ID]
        del insert_data[FieldNameConstants.CREATED_AT]
        del insert_data[FieldNameConstants.UPDATED_AT]
        _body = json.dumps(insert_data)
        # Act
        response = self.fetch(
            APIEndpointV1.CONTACT_URI,
            method=HttpMethodConstants.POST,
            headers=_headers,
            body=_body
        )
        # Assert
        assert response.code == HTTPStatus.CREATED
        assert GenericConstants.HEADER_LOCATION in response.headers
        assert GenericConstants.HEADER_CONTACT_ID in response.headers
        _location = response.headers[GenericConstants.HEADER_LOCATION]
        assert _location is not None
        _contact_id = response.headers[GenericConstants.HEADER_CONTACT_ID]
        assert _contact_id is not None
        assert isinstance(_contact_id, str)
        assert isinstance(_location, str)
        # Clean-Up-Contact
        contact_service = self.get_contact_service()
        assert contact_service.deleteUserContact(
            user_id=user_id, contact_id=_contact_id) is True
        # Clean-Up-User
        assert user_service.deleteUser(user_id=user_id) is True
