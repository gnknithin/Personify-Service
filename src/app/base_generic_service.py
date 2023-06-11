import logging
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from infra.data.unit_of_work.base_unit_of_work import BaseUnitOfWork

T = TypeVar('T')


class BaseGenericService(Generic[T]):
    def __init__(
        self, logger: logging.Logger,
        uow: BaseUnitOfWork[T],
        model_type: Type[T]
    ):
        self._logger = logger
        self._model_type = model_type
        self._unit_of_work = uow

    @property
    def unit_of_work(self) -> BaseUnitOfWork[T]:
        """The uow property."""
        return self._unit_of_work

    def _add(self, data: Type[T]) -> Union[str, None]:
        with self.unit_of_work as _uow:
            return _uow.repository.add(data)

    def _get_by_key(self, key: str) -> Union[Type[T], None]:
        with self.unit_of_work as _uow:
            return _uow.repository.get_by_key(key)

    def _get(
        self, filter_by: Optional[Dict[Any, Any]] = None,
        skip_to: Optional[int] = None,
        limit_by: Optional[int] = None
    ) -> List[Type[T]]:
        with self.unit_of_work as _uow:
            return _uow.repository.get(
                filter_by=filter_by,
                skip_to=skip_to,
                limit_by=limit_by
            )

    def _update(
        self,
        key: str,
        data: Type[T]
    ) -> Union[Type[T], None]:
        with self.unit_of_work as _uow:
            return _uow.repository.update(key=key, data=data)

    def _remove(self, key: str) -> bool:
        with self.unit_of_work as _uow:
            return _uow.repository.remove(key)
