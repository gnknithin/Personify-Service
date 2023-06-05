import logging
from typing import Any, Dict, Generic, List, Optional, Type, Union

from app.abstract_service import AbstractService
from infra.constants._type import TEntityModel, TSQLEntityModel
from infra.data.unit_of_work.mongo_unit_of_work import MongoUnitOfWork
from infra.data.unit_of_work.postgres_unit_of_work import PostgresUnitOfWork


class BaseGenericService(AbstractService, Generic[TEntityModel]):
    def __init__(
        self, logger: logging.Logger,
        uow: MongoUnitOfWork[TEntityModel],
        model_type: Type[TEntityModel]
    ):
        super().__init__(logger=logger)
        self._model_type = model_type
        self._unit_of_work = uow

    @property
    def unit_of_work(self) -> MongoUnitOfWork[TEntityModel]:
        """The uow property."""
        return self._unit_of_work

    def _add(self, data: Type[TEntityModel]) -> Union[str, None]:
        with self.unit_of_work as _uow:
            return _uow.repository.add(data)

    def _get_by_key(self, key: str) -> Union[Type[TEntityModel], None]:
        with self.unit_of_work as _uow:
            return _uow.repository.get_by_key(key)

    def _get(
        self, filter_by: Optional[Dict[Any, Any]] = None,
        skip_to: Optional[int] = 0, limit_by: Optional[int] = 0
    ) -> List[Type[TEntityModel]]:
        with self.unit_of_work as _uow:
            return _uow.repository.get(filter_by=filter_by, skip_to=skip_to, limit_by=limit_by)

    def _update(
        self,
        key: str,
        data: Type[TEntityModel]
    ) -> Union[Type[TEntityModel], None]:
        with self.unit_of_work as _uow:
            return _uow.repository.update(key=key, data=data)

    def _remove(self, key: str) -> bool:
        with self.unit_of_work as _uow:
            return _uow.repository.remove(key)


class BaseSQLGenericService(AbstractService, Generic[TSQLEntityModel]):
    def __init__(
        self, logger: logging.Logger,
        uow: PostgresUnitOfWork[TSQLEntityModel],
        model_type: Type[TSQLEntityModel]
    ):
        super().__init__(logger=logger)
        self._model_type = model_type
        self._unit_of_work = uow

    @property
    def unit_of_work(self) -> PostgresUnitOfWork[TSQLEntityModel]:
        """The uow property."""
        return self._unit_of_work
