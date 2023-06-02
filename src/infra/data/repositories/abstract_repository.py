import logging
from abc import ABC
from typing import Type, Union

from infra.constants._type import TEntity, TEntityModel


class AbstractRepository(ABC):
    def __init__(
        self,
        logger: logging.Logger,
        model_type: Union[Type[TEntity], Type[TEntityModel]]
    ) -> None:
        self._logger = logger
        self._model_type = model_type
