from typing import Type

from bootstrap import ApplicationBootstrap
from infra.constants._type import TSQLEntityModel
from infra.data.unit_of_work.postgres_unit_of_work import PostgresUnitOfWork


class PostgresUnitOfWorkFactory():
    def __init__(self, bootstrap: ApplicationBootstrap) -> None:
        self._bootstrap = bootstrap

    def build(
        self,
        model_type: Type[TSQLEntityModel],
        scope: str
    ) -> PostgresUnitOfWork[TSQLEntityModel]:
        unit_of_work = PostgresUnitOfWork[TSQLEntityModel](
            logger=self._bootstrap.logger,
            db_adapter=self._bootstrap.postgres_adapter,
            model_type=model_type,
            scope=scope
        )
        return unit_of_work
