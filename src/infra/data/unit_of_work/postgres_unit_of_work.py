import logging
from typing import Any, Generic, Type

from infra.adapters.database.postgres.postgres_adapter import PostgresAdapter
from infra.constants._type import TSQLEntityModel
from infra.data.repositories.postgres_repository import PostgresRepository
from infra.data.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork
from sqlalchemy.orm import sessionmaker


class PostgresUnitOfWork(AbstractUnitOfWork, Generic[TSQLEntityModel]):
    def __init__(
        self,
        logger: logging.Logger,
        db_adapter: PostgresAdapter,
        model_type: Type[TSQLEntityModel],
        scope: str
    ) -> None:
        super().__init__(logger=logger)
        self._model_type = model_type
        self._session_factory = sessionmaker(db_adapter.engine)
        self._session = self._session_factory()
        self._scope = scope

        self._repository = PostgresRepository[TSQLEntityModel](
            logger=self._logger,
            session=self.session,
            model_type=self._model_type
        )

    @property
    def repository(self) -> PostgresRepository[TSQLEntityModel]:
        """The repository property."""
        _msg = "{0} Ids - Scope: {1} - UoW id: {2} - session id: {3}".format(
            self.__class__.__name__,
            self._scope,
            id(self),
            id(self.session)
        )
        self._logger.info(msg=_msg)

        return self._repository

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def __enter__(self):
        _msg = "{0} Context Manager Scope started - Scope: {1}".format(
            self.__class__.__name__,
            self._scope
        )
        self._logger.info(msg=_msg)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        super().__exit__(exc_type, exc_val, exc_tb)

        self.session.close()
