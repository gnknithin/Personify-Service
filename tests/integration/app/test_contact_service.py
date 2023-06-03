from random import choice
from typing import Any, Dict, List, Type
from uuid import UUID

from app.factory.build_contact_service import ContactServiceFactory
from bootstrap import ApplicationBootstrap
from domain.contact_model import ContactModel
from infra.constants._string import FieldNameConstants

from tests.utils.base_tests import BaseIntegrationTest
from tests.utils.core_seed import ContactSeed


class TestContactService(BaseIntegrationTest):
    SCOPE = 'integration-test-contact-service'

    def _create_records(self, size: int) -> List[Dict[Any, Any]]:
        return ContactSeed.create_seed(size=size)

    def test_should_add_delete_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        contact_service = ContactServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        seed_contact_data = self._create_records(size=1)[0]
        seed_user_id = seed_contact_data[FieldNameConstants.USER_ID]
        del seed_contact_data[FieldNameConstants.OBJECT_ID]
        del seed_contact_data[FieldNameConstants.USER_ID]
        del seed_contact_data[FieldNameConstants.CREATED_AT]
        del seed_contact_data[FieldNameConstants.UPDATED_AT]
        seed_contact_model: Dict[
            Any, Any
        ] = ContactModel().load(
            data=seed_contact_data,
            partial=(
                FieldNameConstants.USER_ID,
            )
        )
        # Act
        sut = contact_service.addUserContact(
            user_id=seed_user_id,
            data=seed_contact_model
        )
        # Assert
        assert sut is not None
        assert isinstance(sut, str)
        # Clean-Up
        assert contact_service.deleteUserContact(
            user_id=seed_user_id,
            contact_id=sut
        ) is True

    def test_should_update_delete_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        contact_service = ContactServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        seed_data = self._create_records(size=1)[0]
        seed_user_id = seed_data[FieldNameConstants.USER_ID]

        create_data: Dict[Any, Any] = dict()
        create_data[
            FieldNameConstants.FULL_NAME
        ] = seed_data[FieldNameConstants.FULL_NAME]

        del seed_data[FieldNameConstants.OBJECT_ID]
        del seed_data[FieldNameConstants.USER_ID]
        del seed_data[FieldNameConstants.CREATED_AT]
        del seed_data[FieldNameConstants.UPDATED_AT]

        seed_contact_model = ContactModel().load(
            data=create_data,
            partial=(
                FieldNameConstants.USER_ID,
            )
        )
        # Arrange
        contact_id: str = contact_service.addUserContact(
            user_id=seed_user_id,
            data=seed_contact_model
        )
        assert contact_id is not None
        update_data = ContactModel().load(
            data=seed_data,
            partial=(
                FieldNameConstants.USER_ID,
            )
        )
        # Act
        sut = contact_service.updateUserContact(
            user_id=seed_user_id,
            contact_id=contact_id,
            data=update_data
        )
        # Assert
        assert sut is not None
        assert isinstance(sut, Dict)
        # Clean-Up
        assert contact_service.deleteUserContact(
            user_id=seed_user_id,
            contact_id=contact_id
        ) is True

    def test_should_use_get_and_get_by_key_and_delete_successfuly(
        self,
        init_bootstrap: ApplicationBootstrap
    ):
        # Arrange
        contact_service = ContactServiceFactory(
            bootstrap=init_bootstrap
        ).build(scope=self.SCOPE)
        seed_contact_data = self._create_records(size=10)
        seed_user_id: UUID = seed_contact_data[0][FieldNameConstants.USER_ID]
        created_contact_ids: List[str] = list()
        for each in seed_contact_data:
            del each[FieldNameConstants.OBJECT_ID]
            del each[FieldNameConstants.USER_ID]
            del each[FieldNameConstants.CREATED_AT]
            del each[FieldNameConstants.UPDATED_AT]
            each_contact_model = ContactModel().load(
                data=each, partial=(FieldNameConstants.USER_ID,))
            contact_id: str = contact_service.addUserContact(
                user_id=seed_user_id,
                data=each_contact_model
            )
            created_contact_ids.append(contact_id)

        # Act
        sut = contact_service.getUserContacts(user_id=seed_user_id)
        # Assert
        assert sut is not None
        assert isinstance(sut, List)
        # sut-Get-By-Key
        sut_get_by_key = contact_service.getUserContactById(
            user_id=seed_user_id,
            contact_id=choice(created_contact_ids)
        )
        assert sut_get_by_key is not None
        assert isinstance(sut_get_by_key, dict)
        # Clean-Up
        for each in created_contact_ids:
            assert contact_service.deleteUserContact(
                user_id=seed_user_id,
                contact_id=each
            ) is True
