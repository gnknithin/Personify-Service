from bootstrap import ApplicationBootstrap

from tests.utils.base_tests import BaseIntegrationTest


class TestMinIOAdminAdapter(BaseIntegrationTest):
    def test_should_check_server_info(
        self, init_bootstrap: ApplicationBootstrap
    ) -> None:
        # Arrange
        _minio_admin_adapter = init_bootstrap.minio_admin_adapter
        # Act
        sut = _minio_admin_adapter.info()
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
