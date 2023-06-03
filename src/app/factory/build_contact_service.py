from app.contact_service import ContactService
from bootstrap import ApplicationBootstrap
from domain.contact_model import ContactModel
from infra.constants._string import ApplicationConstants
from infra.data.unit_of_work.mongo_unit_of_work import MongoUnitOfWork


class ContactServiceFactory():
    def __init__(self, bootstrap: ApplicationBootstrap) -> None:
        self._bootstrap = bootstrap

    def build(self, scope: str) -> ContactService:

        _mongo_uow = MongoUnitOfWork(
            logger=self._bootstrap.logger,
            db_adapter=self._bootstrap.mongo_adapter,
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