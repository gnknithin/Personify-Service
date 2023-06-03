import logging
from abc import ABC


class AbstractService(ABC):
    """docstring for AbstractService."""

    def __init__(self, logger: logging.Logger):
        self._logger = logger
