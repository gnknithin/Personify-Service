import logging
from typing import Generic, TypeVar

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(
        self,
        logger: logging.Logger
    ) -> None:
        self._logger = logger
