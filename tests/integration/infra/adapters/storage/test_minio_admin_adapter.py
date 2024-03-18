import os
from random import choice
from typing import List

import pytest
from bootstrap import ApplicationBootstrap
from infra.constants._string import MinioConstants
from infra.generator.identity import IdentityGenerator
from minio.error import MinioAdminException

from tests.utils.base_tests import BaseIntegrationTest


class TestMinIOAdminAdapter(BaseIntegrationTest):
    def test_should_check_server_info(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _minio_admin_adapter = init_bootstrap.minio_admin_adapter
        # Act
        sut = _minio_admin_adapter.server_info()
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)

    def test_should_check_server_availability(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _minio_admin_adapter = init_bootstrap.minio_admin_adapter
        # Act
        sut = _minio_admin_adapter.check_avilability()
        # Assert
        assert sut is not None
        assert isinstance(sut, bool)
        assert sut is True

    def test_should_delete_random_user_raise_MinioAdminException(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _minio_admin_adapter = init_bootstrap.minio_admin_adapter
        _random_access_key = f"{IdentityGenerator().get_random_id()}"
        # Act
        with pytest.raises(MinioAdminException) as exec_info:
            _ = _minio_admin_adapter.delete_user(user_access_key=_random_access_key)
            assert exec_info.type is MinioAdminException

    def test_should_add_existing_user_and_return_successfully(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _minio_admin_adapter = init_bootstrap.minio_admin_adapter
        _random_access_key = f"{IdentityGenerator().get_random_id()}"
        _random_secret_key = f"{IdentityGenerator().get_random_id()}"
        _create_user = _minio_admin_adapter.add_user(
            user_access_key=_random_access_key, user_secret_key=_random_secret_key
        )
        assert _create_user is not None
        assert isinstance(_create_user, str)
        # Act
        sut = _minio_admin_adapter.add_user(
            user_access_key=_random_access_key,
            user_secret_key=_random_secret_key,
        )
        # Assert
        assert sut is not None
        assert isinstance(sut, str)
        # Clean-Up
        _delete_user = _minio_admin_adapter.delete_user(
            user_access_key=_random_access_key
        )
        assert _delete_user is not None
        assert isinstance(_delete_user, str)

    def test_should_delete_existing_user_and_return_successfully(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _minio_admin_adapter = init_bootstrap.minio_admin_adapter
        _random_access_key = f"{IdentityGenerator().get_random_id()}"
        _random_secret_key = f"{IdentityGenerator().get_random_id()}"
        _create_user = _minio_admin_adapter.add_user(
            user_access_key=_random_access_key, user_secret_key=_random_secret_key
        )
        assert _create_user is not None
        assert isinstance(_create_user, str)
        # Act
        sut = _minio_admin_adapter.delete_user(user_access_key=_random_access_key)
        # Assert
        assert sut is not None
        assert isinstance(sut, str)

    def test_should_get_random_user_info_raise_MinioAdminException(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _minio_admin_adapter = init_bootstrap.minio_admin_adapter
        _random_access_key = f"{IdentityGenerator().get_random_id()}"
        # Act
        with pytest.raises(MinioAdminException) as exec_info:
            _ = _minio_admin_adapter.get_user_info(user_access_key=_random_access_key)
            assert exec_info.type is MinioAdminException

    def test_should_get_existing_user_info_and_return_successfully(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _minio_admin_adapter = init_bootstrap.minio_admin_adapter
        _random_access_key = f"{IdentityGenerator().get_random_id()}"
        _random_secret_key = f"{IdentityGenerator().get_random_id()}"
        _create_user = _minio_admin_adapter.add_user(
            user_access_key=_random_access_key, user_secret_key=_random_secret_key
        )
        assert _create_user is not None
        assert isinstance(_create_user, str)
        # Act
        sut = _minio_admin_adapter.get_user_info(user_access_key=_random_access_key)
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)
        assert "status" in sut
        assert isinstance(sut["status"], str)
        # Clean-Up
        _delete_user = _minio_admin_adapter.delete_user(
            user_access_key=_random_access_key
        )
        assert _delete_user is not None
        assert isinstance(_delete_user, str)

    def test_should_disable_user(self, init_bootstrap: ApplicationBootstrap) -> None:
        # Arrange
        _minio_admin_adapter = init_bootstrap.minio_admin_adapter
        _random_access_key = f"{IdentityGenerator().get_random_id()}"
        _random_secret_key = f"{IdentityGenerator().get_random_id()}"
        _create_user = _minio_admin_adapter.add_user(
            user_access_key=_random_access_key, user_secret_key=_random_secret_key
        )
        assert _create_user is not None
        assert isinstance(_create_user, str)
        _user_enabled = _minio_admin_adapter.is_user_enabled(
            user_access_key=_random_access_key
        )
        assert _user_enabled is not None
        assert isinstance(_user_enabled, bool)
        assert _user_enabled is True
        # Act
        sut = _minio_admin_adapter.disable_user(user_access_key=_random_access_key)
        # Assert
        assert sut is not None
        assert isinstance(sut, str)
        _user_disabled = _minio_admin_adapter.is_user_enabled(
            user_access_key=_random_access_key
        )
        assert _user_disabled is not None
        assert isinstance(_user_disabled, bool)
        assert _user_disabled is False
        # Clean-Up
        _delete_user = _minio_admin_adapter.delete_user(
            user_access_key=_random_access_key
        )
        assert _delete_user is not None
        assert isinstance(_delete_user, str)

    def test_should_check_random_user_enabled_and_raise_MinioAdminException(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _minio_admin_adapter = init_bootstrap.minio_admin_adapter
        _random_access_key = f"{IdentityGenerator().get_random_id()}"
        # Act
        with pytest.raises(MinioAdminException) as exec_info:
            _ = _minio_admin_adapter.is_user_enabled(user_access_key=_random_access_key)
            assert exec_info.type is MinioAdminException

    def test_should_check_is_user_enabled_and_return_true(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _minio_admin_adapter = init_bootstrap.minio_admin_adapter
        _random_access_key = f"{IdentityGenerator().get_random_id()}"
        _random_secret_key = f"{IdentityGenerator().get_random_id()}"
        _create_user = _minio_admin_adapter.add_user(
            user_access_key=_random_access_key, user_secret_key=_random_secret_key
        )
        assert _create_user is not None
        assert isinstance(_create_user, str)
        # Act
        sut = _minio_admin_adapter.is_user_enabled(user_access_key=_random_access_key)
        # Assert
        assert sut is not None
        assert isinstance(sut, bool)
        # Clean-Up
        _delete_user = _minio_admin_adapter.delete_user(
            user_access_key=_random_access_key
        )
        assert _delete_user is not None
        assert isinstance(_delete_user, str)

    def test_should_get_existing_users(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _app_user_access_key = os.environ.get(
            MinioConstants.ENVVAR_MINIO_APP_USER_ACCESS_KEY
        )
        assert _app_user_access_key is not None
        _minio_admin_adapter = init_bootstrap.minio_admin_adapter
        _user_ids: List[str] = list()
        _user_ids.append(_app_user_access_key)
        for _ in range(10):
            _random_access_key = f"{IdentityGenerator().get_random_id()}"
            _random_secret_key = f"{IdentityGenerator().get_random_id()}"
            _create_user = _minio_admin_adapter.add_user(
                user_access_key=_random_access_key, user_secret_key=_random_secret_key
            )
            assert _create_user is not None
            assert isinstance(_create_user, str)
            _user_ids.append(_random_access_key)
        # Act
        sut = _minio_admin_adapter.get_users()
        # Assert
        assert sut is not None
        assert isinstance(sut, dict)
        for _each_user_access_key, _each_user_status_dict in sut.items():
            assert _each_user_access_key is not None
            assert isinstance(_each_user_access_key, str)
            assert _each_user_access_key in _user_ids
            assert _each_user_status_dict is not None
            assert isinstance(_each_user_status_dict, dict)
            assert "status" in _each_user_status_dict
            assert isinstance(_each_user_status_dict["status"], str)

        # Clean-Up
        for _each_user_access_key in _user_ids:
            _delete_user = _minio_admin_adapter.delete_user(
                user_access_key=_each_user_access_key
            )
            assert _delete_user is not None
            assert isinstance(_delete_user, str)

    def test_should_check_existing_user_return_true(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _minio_admin_adapter = init_bootstrap.minio_admin_adapter
        _user_ids: List[str] = list()
        for _ in range(2):
            _random_access_key = f"{IdentityGenerator().get_random_id()}"
            _random_secret_key = f"{IdentityGenerator().get_random_id()}"
            _create_user = _minio_admin_adapter.add_user(
                user_access_key=_random_access_key, user_secret_key=_random_secret_key
            )
            assert _create_user is not None
            assert isinstance(_create_user, str)
            _user_ids.append(_random_access_key)
        # Act
        sut = _minio_admin_adapter.check_user_exists(user_access_key=choice(_user_ids))
        # Assert
        assert sut is not None
        assert isinstance(sut, bool)
        assert sut is True

        # Clean-Up
        for _each_user_access_key in _user_ids:
            _delete_user = _minio_admin_adapter.delete_user(
                user_access_key=_each_user_access_key
            )
            assert _delete_user is not None
            assert isinstance(_delete_user, str)

    def test_should_check_existing_user_return_false(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _minio_admin_adapter = init_bootstrap.minio_admin_adapter
        _random_access_key = f"{IdentityGenerator().get_random_id()}"
        # Act
        sut = _minio_admin_adapter.check_user_exists(user_access_key=_random_access_key)
        # Assert
        assert sut is not None
        assert isinstance(sut, bool)
        assert sut is False
