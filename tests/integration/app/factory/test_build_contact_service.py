from app.contact_service import ContactService
from app.factory.build_contact_service import ContactServiceFactory
from bootstrap import ApplicationBootstrap

from tests.utils.base_tests import BaseIntegrationTest


class TestContactServiceFactory(BaseIntegrationTest):
    SCOPE = 'integration-test-contact-service-factory'

    def test_should_return_instance_of_contact_service(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        # Act
        sut = ContactServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        assert sut is not None
        assert isinstance(sut, ContactService)
