from random import choice
from typing import Any, Dict, List, Optional
from uuid import UUID

from app.factory.build_user_service import UserServiceFactory
from bootstrap import ApplicationBootstrap
from domain.contact_model import ContactModel
from infra.constants._string import FieldNameConstants

from tests.utils.base_tests import BaseIntegrationTest
from tests.utils.core_seed import UserSeed


class TestUserService(BaseIntegrationTest):
    SCOPE = 'integration-test-user-service'

    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return UserSeed.create_seed(size=size)

    def test_should_add_delete_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # TODO
        '''
        # Arrange
        user_service = UserServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        seed_user_data = self._create_records(size=1)[0]

        # Act
        sut = user_service.add()
        # Assert
        assert sut is not None
        assert isinstance(sut, str)
        # Clean-Up
        assert user_service.deleteUserContact() is True
        '''
