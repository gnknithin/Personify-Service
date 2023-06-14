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
from infra.generator.identity import IdentityGenerator

from tests.utils.base_tests import MainApplicationTestSetup
from tests.utils.core_seed import ContactSeed, UserSeed


class TestContactIdHandlerGetMethod(MainApplicationTestSetup):

    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return ContactSeed.create_seed(size=size)

    def _create_user_records(self, size: int) -> List[Dict[Any, Any]]:
        return UserSeed.create_seed(size=size)

    def test_get_method_with_invalid_contact_id_successfully(self):
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
        # Arrange-Contact-Id
        _contact_id = IdentityGenerator.get_random_id_of_object_length()
        assert _contact_id is not None
        # Act
        _contact_id_uri = APIEndpointV1.CONTACT_BY_ID_URI.replace(
            '{contact_id}', _contact_id
        )
        response = self.fetch(
            _contact_id_uri,
            method=HttpMethodConstants.GET,
            headers=_headers,
            body=None
        )
        # Assert
        assert response.code == HTTPStatus.BAD_REQUEST
        decoded_body = json.loads(response.body.decode(GenericConstants.UTF8))
        assert decoded_body is not None
        assert isinstance(decoded_body, dict)
        assert GenericConstants.SUCCESS in decoded_body
        assert isinstance(decoded_body[GenericConstants.SUCCESS], bool)
        assert decoded_body[GenericConstants.SUCCESS] is False
        assert GenericConstants.ERRORS in decoded_body
        assert isinstance(decoded_body[GenericConstants.ERRORS], list)
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
        # Arrange-Insert-Contact-Data
        insert_data: Dict[Any, Any] = self._create_records(size=1)[0]
        del insert_data[FieldNameConstants.OBJECT_ID]
        del insert_data[FieldNameConstants.USER_ID]
        del insert_data[FieldNameConstants.CREATED_AT]
        del insert_data[FieldNameConstants.UPDATED_AT]
        _insert_contact = ContactModel().load(
            data=insert_data,
            partial=(
                FieldNameConstants.USER_ID,
            )
        )
        # Arrange-Contact
        contact_service = self.get_contact_service()
        # Arrange-Contact-Id
        _contact_id = contact_service.addUserContact(
            user_id=user_id, data=_insert_contact
        )
        assert _contact_id is not None
        # Act
        _contact_id_uri = APIEndpointV1.CONTACT_BY_ID_URI.replace(
            '{contact_id}', _contact_id
        )
        response = self.fetch(
            _contact_id_uri,
            method=HttpMethodConstants.GET,
            headers=_headers,
            body=None
        )
        # Assert
        assert response.code == HTTPStatus.OK
        decoded_body = json.loads(response.body.decode(GenericConstants.UTF8))
        assert decoded_body is not None
        assert isinstance(decoded_body, dict)
        assert GenericConstants.SUCCESS in decoded_body
        assert isinstance(decoded_body[GenericConstants.SUCCESS], bool)
        assert decoded_body[GenericConstants.SUCCESS] is True
        assert GenericConstants.DATA in decoded_body
        assert isinstance(decoded_body[GenericConstants.DATA], dict)
        _contact = decoded_body[GenericConstants.DATA]
        assert FieldNameConstants.FULL_NAME in _contact
        assert FieldNameConstants.BIRTHDAY in _contact
        assert FieldNameConstants.UPDATED_AT in _contact
        assert FieldNameConstants.CREATED_AT in _contact
        assert FieldNameConstants.CONTACT_ID in _contact
        assert FieldNameConstants.EMAIL in _contact
        assert FieldNameConstants.MOBILE in _contact
        assert isinstance(_contact[FieldNameConstants.FULL_NAME], str)
        assert isinstance(_contact[FieldNameConstants.BIRTHDAY], str)
        assert isinstance(_contact[FieldNameConstants.UPDATED_AT], str)
        assert isinstance(_contact[FieldNameConstants.CREATED_AT], str)
        assert isinstance(_contact[FieldNameConstants.CONTACT_ID], str)
        assert isinstance(_contact[FieldNameConstants.EMAIL], str)
        assert isinstance(_contact[FieldNameConstants.MOBILE], str)
        # Clean-Up-Contact
        assert contact_service.deleteUserContact(
            user_id=user_id, contact_id=_contact_id) is True
        # Clean-Up-User
        assert user_service.deleteUser(user_id=user_id) is True
