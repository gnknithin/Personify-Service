from app.factory.build_user_service import UserServiceFactory
from app.user_service import UserService
from bootstrap import ApplicationBootstrap

from tests.utils.base_tests import BaseIntegrationTest


class TestUserServiceFactory(BaseIntegrationTest):
    SCOPE = 'integration-test-user-service-factory'

    def test_should_return_instance_of_user_service(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        # Act
        sut = UserServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        assert sut is not None
        assert isinstance(sut, UserService)
