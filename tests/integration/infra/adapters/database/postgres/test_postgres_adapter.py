from bootstrap import ApplicationBootstrap

from tests.utils.base_tests import BaseIntegrationTest


class TestPostgresAdapter(BaseIntegrationTest):

    def test_should_check_availability_successfully(
        self, init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        _postgres_adapter = init_bootstrap.postgres_adapter
        # Act
        sut = _postgres_adapter.check_availability()
        # Assert
        assert sut is True
