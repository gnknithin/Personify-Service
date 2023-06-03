import logging
from abc import ABC


class AbstractRepository(ABC):
    def __init__(
        self,
        logger: logging.Logger
    ) -> None:
        self._logger = logger
