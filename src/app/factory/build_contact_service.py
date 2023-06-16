from app.contact_service import ContactService
from app.factory.build_base_service import BaseServiceFactory
from bootstrap import ApplicationBootstrap
from domain.contact_model import ContactModel
from infra.constants._string import ApplicationConstants
from infra.data.unit_of_work.factory.build_mongo_uow import MongoUnitOfWorkFactory


class ContactServiceFactory(BaseServiceFactory):
    def __init__(self, bootstrap: ApplicationBootstrap) -> None:
        super().__init__(bootstrap=bootstrap)

    def build(self, scope: str) -> ContactService:

        _mongo_uow = MongoUnitOfWorkFactory(bootstrap=self._bootstrap).build(
            db_name=ApplicationConstants.DATABSE_NAME_PERSONIFY,
            collection_name=ApplicationConstants.COLLECTION_NAME_CONTACTS,
            model_type=ContactModel,
            scope=scope
        )

        contact_service = ContactService(
            logger=self._bootstrap.logger,
            uow=_mongo_uow,
            model_type=ContactModel

        )
        return contact_service
