from typing import Type

from bootstrap import ApplicationBootstrap
from infra.constants._type import TEntityModel
from infra.data.unit_of_work.mongo_unit_of_work import MongoUnitOfWork


class MongoUnitOfWorkFactory():
    def __init__(self, bootstrap: ApplicationBootstrap) -> None:
        self._bootstrap = bootstrap

    def build(
        self,
        db_name: str,
        collection_name: str,
        model_type: Type[TEntityModel],
        scope: str
    ) -> MongoUnitOfWork[TEntityModel]:
        unit_of_work = MongoUnitOfWork[TEntityModel](
            logger=self._bootstrap.logger,
            db_adapter=self._bootstrap.mongo_adapter,
            db_name=db_name,
            collection_name=collection_name,
            model_type=model_type,
            scope=scope
        )

        return unit_of_work
