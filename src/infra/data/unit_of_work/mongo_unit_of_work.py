import logging
from typing import Any, Generic, Type

from infra.adapters.database.mongo.pymongo_adapter import PyMongoAdapter
from infra.constants._type import TEntityModel
from infra.data.repositories.mongo_repository import MongoRepository
from infra.data.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork


class MongoUnitOfWork(AbstractUnitOfWork, Generic[TEntityModel]):
    def __init__(
        self,
        logger: logging.Logger,
        db_adapter: PyMongoAdapter,
        db_name: str,
        collection_name: str,
        model_type: Type[TEntityModel],
        scope: str = ''
    ) -> None:
        super().__init__(logger=logger)
        self._model_type = model_type
        self._db_client = db_adapter
        self._scope = scope
        self._repository = MongoRepository[TEntityModel](
            logger=self._logger,
            db_adapter=self._db_client,
            database_name=db_name,
            collection_name=collection_name,
            model_type=self._model_type,
        )

    @property
    def repository(self) -> MongoRepository[TEntityModel]:
        """The repository property."""
        self._logger.info(
            msg=f'{self.__class__.__name__} Ids - Scope: {self._scope} - UoW id: {id(self)}')

        return self._repository

    def commit(self) -> Any:
        pass

    def rollback(self) -> Any:
        pass

    def __enter__(self):
        self._logger.info(
            msg=f'{self.__class__.__name__} Context Manager Scope started - Scope: {self._scope}')
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        super().__exit__(exc_type, exc_val, exc_tb)
