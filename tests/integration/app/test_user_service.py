from typing import Any, Dict, List
from uuid import UUID

from app.factory.build_user_service import UserServiceFactory
from bootstrap import ApplicationBootstrap
from domain.user_model import UserModel
from infra.constants._string import FieldNameConstants

from tests.utils.base_tests import BaseIntegrationTest
from tests.utils.core_seed import UserSeed


class TestUserService(BaseIntegrationTest):
    SCOPE = 'integration-test-user-service'

    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return UserSeed.create_seed(size=size)

    def test_should_return_none_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        user_service = UserServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        seed_user_data = self._create_records(size=1)[0]
        del seed_user_data[FieldNameConstants.CREATED_AT]
        del seed_user_data[FieldNameConstants.UPDATED_AT]
        del seed_user_data[FieldNameConstants.OBJECT_ID]
        _user_model = UserModel(**seed_user_data)
        user_id = user_service.createUser(data=_user_model)
        assert isinstance(user_id, UUID)
        _again_user_model = UserModel(**seed_user_data)
        # Act
        sut = user_service.createUser(data=_again_user_model)
        # Assert
        assert sut is None
        # Clean-Up
        assert user_service.deleteUser(user_id=user_id) is True

    def test_should_createUser_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        user_service = UserServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        seed_user_data = self._create_records(size=1)[0]
        del seed_user_data[FieldNameConstants.CREATED_AT]
        del seed_user_data[FieldNameConstants.UPDATED_AT]
        del seed_user_data[FieldNameConstants.OBJECT_ID]
        _user_model = UserModel(**seed_user_data)
        # Act
        sut = user_service.createUser(data=_user_model)
        # Assert
        assert sut is not None
        assert isinstance(sut, UUID)
        # Clean-Up
        assert user_service.deleteUser(user_id=sut) is True

    def test_should_deleteUser_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        user_service = UserServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        seed_user_data = self._create_records(size=1)[0]
        del seed_user_data[FieldNameConstants.CREATED_AT]
        del seed_user_data[FieldNameConstants.UPDATED_AT]
        del seed_user_data[FieldNameConstants.OBJECT_ID]
        _user_model = UserModel(**seed_user_data)
        user_id = user_service.createUser(data=_user_model)
        assert user_id is not None
        assert isinstance(user_id, UUID)
        # Act
        sut = user_service.deleteUser(user_id=user_id)
        # Assert
        assert sut is True
        # Clean-Up

    def test_should_getUserById_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        user_service = UserServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        seed_user_data = self._create_records(size=1)[0]
        del seed_user_data[FieldNameConstants.CREATED_AT]
        del seed_user_data[FieldNameConstants.UPDATED_AT]
        del seed_user_data[FieldNameConstants.OBJECT_ID]
        _user_model = UserModel(**seed_user_data)
        user_id = user_service.createUser(data=_user_model)
        assert user_id is not None
        assert isinstance(user_id, UUID)
        # Act
        sut = user_service.getUserById(user_id=user_id)
        # Assert
        assert sut is not None
        # TODO Check All Values
        # Clean-Up
        assert user_service.deleteUser(user_id=user_id) is True

    def test_should_check_findByUserName_and_return_none_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        user_service = UserServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        seed_user_data = self._create_records(size=1)[0]
        _user_name = seed_user_data[FieldNameConstants.USERNAME]
        # Act
        sut = user_service.findByUserName(
            userName=_user_name
        )
        # Assert
        assert sut is None

    def test_should_check_findByUserName_and_return_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        user_service = UserServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        seed_user_data = self._create_records(size=1)[0]
        _user_name = seed_user_data[FieldNameConstants.USERNAME]
        del seed_user_data[FieldNameConstants.CREATED_AT]
        del seed_user_data[FieldNameConstants.UPDATED_AT]
        del seed_user_data[FieldNameConstants.OBJECT_ID]
        _user_model = UserModel(**seed_user_data)
        user_id = user_service.createUser(data=_user_model)
        assert user_id is not None
        assert isinstance(user_id, UUID)
        # Act
        sut = user_service.findByUserName(
            userName=_user_name
        )
        # Assert
        assert sut is not None
        # TODO Check All Values
        assert hasattr(sut, FieldNameConstants.USERNAME)
        assert sut.username == _user_name
        # Clean-Up
        assert user_service.deleteUser(user_id=user_id) is True

    def test_should_check_loginUserWithInvalidUserName_and_return_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        user_service = UserServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        seed_user_data = self._create_records(size=1)[0]
        _login: Dict[Any, Any] = dict()
        _login[
            FieldNameConstants.USERNAME
        ] = seed_user_data[FieldNameConstants.USERNAME]
        _login[
            FieldNameConstants.PASSWORD
        ] = seed_user_data[FieldNameConstants.PASSWORD]
        _login_user = UserModel(**_login)
        # Act
        sut = user_service.loginUserWithCredentials(data=_login_user)
        # Assert
        assert sut is not None
        assert isinstance(sut, list)
        assert len(sut) == 1

    def test_should_check_loginUserWithInvalidPassword_and_return_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        user_service = UserServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        seed_user_data = self._create_records(size=1)[0]
        del seed_user_data[FieldNameConstants.CREATED_AT]
        del seed_user_data[FieldNameConstants.UPDATED_AT]
        del seed_user_data[FieldNameConstants.OBJECT_ID]
        _user_model = UserModel(**seed_user_data)
        user_id = user_service.createUser(data=_user_model)
        assert user_id is not None
        assert isinstance(user_id, UUID)
        _login: Dict[Any, Any] = dict()
        _login[
            FieldNameConstants.USERNAME
        ] = seed_user_data[FieldNameConstants.USERNAME]
        _login[
            FieldNameConstants.PASSWORD
        ] = 'wrong-password'
        _login_user = UserModel(**_login)
        # Act
        sut = user_service.loginUserWithCredentials(data=_login_user)
        # Assert
        assert sut is not None
        assert isinstance(sut, list)
        assert len(sut) == 1
        # Clean-Up
        assert user_service.deleteUser(user_id=user_id) is True

    def test_should_check_loginUserWithCredentials_and_return_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        user_service = UserServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        seed_user_data = self._create_records(size=1)[0]
        del seed_user_data[FieldNameConstants.CREATED_AT]
        del seed_user_data[FieldNameConstants.UPDATED_AT]
        del seed_user_data[FieldNameConstants.OBJECT_ID]
        _user_model = UserModel(**seed_user_data)
        user_id = user_service.createUser(data=_user_model)
        assert user_id is not None
        assert isinstance(user_id, UUID)
        _login: Dict[Any, Any] = dict()
        _login[
            FieldNameConstants.USERNAME
        ] = seed_user_data[FieldNameConstants.USERNAME]
        _login[
            FieldNameConstants.PASSWORD
        ] = seed_user_data[FieldNameConstants.PASSWORD]
        _login_user = UserModel(**_login)
        # Act
        sut = user_service.loginUserWithCredentials(data=_login_user)
        # Assert
        assert sut is not None
        assert isinstance(sut, str)
        # Clean-Up
        assert user_service.deleteUser(user_id=user_id) is True
