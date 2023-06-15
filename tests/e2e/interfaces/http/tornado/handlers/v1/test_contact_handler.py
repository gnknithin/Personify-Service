import json
from http import HTTPStatus
from typing import Any, Dict, List
from uuid import UUID

from domain.contact_model import ContactModel
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
        ] = "Bearer eyJhbGciOiJIUzI1NiJ9eyJoZWxsbyI6IndvcmxkIn0"
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


class TestContactHandlerGetMethod(MainApplicationTestSetup):
    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return ContactSeed.create_seed(size=size)

    def _create_user_records(self, size: int) -> List[Dict[Any, Any]]:
        return UserSeed.create_seed(size=size)

    def test_get_method_with_wrong_parameters_values_and_return_as_no_content(self):
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
        # Act
        LIMIT = 10
        OFFSET = 'hello'
        QUERY_URL = f'{APIEndpointV1.CONTACT_URI}?limit={LIMIT}&offset={OFFSET}'
        # Act
        response = self.fetch(
            QUERY_URL,
            method=HttpMethodConstants.GET,
            headers=_headers,
            body=None
        )
        # Assert
        assert response.code == HTTPStatus.BAD_REQUEST
        assert response.reason == HTTPStatus.BAD_REQUEST.phrase
        decoded_body = json.loads(response.body.decode(GenericConstants.UTF8))
        assert decoded_body is not None
        assert isinstance(decoded_body, dict)
        assert len(decoded_body) == 2
        assert GenericConstants.SUCCESS in decoded_body
        assert isinstance(decoded_body[GenericConstants.SUCCESS], bool)
        assert decoded_body[GenericConstants.SUCCESS] is False
        assert GenericConstants.ERRORS in decoded_body
        assert isinstance(decoded_body[GenericConstants.ERRORS], list)
        # Clean-Up-User
        assert user_service.deleteUser(user_id=user_id) is True

    def test_get_method_no_content_successfully(self):
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
        # Act
        response = self.fetch(
            APIEndpointV1.CONTACT_URI,
            method=HttpMethodConstants.GET,
            headers=_headers,
            body=None
        )
        # Assert
        assert response.code == HTTPStatus.NO_CONTENT
        # Clean-Up-User
        assert user_service.deleteUser(user_id=user_id) is True

    def test_get_method_successfully(self):
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
        # Arrange-Contact
        contact_service = self.get_contact_service()
        # Arrange-Insert-Contact-Data
        seed_insert_data: List[Dict[Any, Any]] = self._create_records(size=6)
        _inserted_ids: List[str] = list()
        for each in seed_insert_data:
            del each[FieldNameConstants.OBJECT_ID]
            del each[FieldNameConstants.USER_ID]
            del each[FieldNameConstants.CREATED_AT]
            del each[FieldNameConstants.UPDATED_AT]
            _insert_contact = ContactModel().load(
                data=each,
                partial=(
                    FieldNameConstants.USER_ID,
                )
            )
            # Arrange-Contact-Id
            _contact_id = contact_service.addUserContact(
                user_id=user_id, data=_insert_contact
            )
            assert _contact_id is not None
            _inserted_ids.append(_contact_id)
        # Act
        LIMIT = 4
        OFFSET = 1
        QUERY_URL = f'{APIEndpointV1.CONTACT_URI}?limit={LIMIT}&offset={OFFSET}'
        response = self.fetch(
            QUERY_URL,
            method=HttpMethodConstants.GET,
            headers=_headers,
            body=None
        )
        # Assert
        assert response.code == HTTPStatus.OK
        assert response.reason == HTTPStatus.OK.phrase
        decoded_body = json.loads(response.body.decode(GenericConstants.UTF8))
        assert decoded_body is not None
        assert isinstance(decoded_body, dict)
        assert len(decoded_body) == 2
        assert GenericConstants.SUCCESS in decoded_body
        assert isinstance(decoded_body[GenericConstants.SUCCESS], bool)
        assert decoded_body[GenericConstants.SUCCESS] is True
        assert GenericConstants.DATA in decoded_body
        assert isinstance(decoded_body[GenericConstants.DATA], list)
        assert len(decoded_body[GenericConstants.DATA]) == LIMIT

        # Clean-Up-Contacts
        for each_id in _inserted_ids:
            contact_service.deleteUserContact(
                user_id=user_id, contact_id=each_id) is True
        # Clean-Up-User
        assert user_service.deleteUser(user_id=user_id) is True
