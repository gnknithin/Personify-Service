import logging
from abc import abstractmethod
from typing import Any, Generic, Type, TypeVar

from infra.constants._type import TEntity

T = TypeVar('T')


class BaseUnitOfWork(Generic[T]):
    def __init__(
        self,
        logger: logging.Logger,
        model_type: Type[TEntity]
    ) -> None:
        super().__init__()
        self._logger = logger
        self._model_type = model_type
        self._session = None

    @property
    def session(self) -> Any:
        return self._session

    @abstractmethod
    def commit(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> Any:
        raise NotImplementedError

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        if exc_type is None:
            self.commit()
        else:
            self._logger.exception(exc_val)
            self.rollback()
