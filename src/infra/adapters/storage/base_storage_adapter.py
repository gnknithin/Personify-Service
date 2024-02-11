import logging
from abc import abstractmethod

from infra.adapters.base_adapter import BaseAdapter


class BaseStorageAdapter(BaseAdapter):
    def __init__(self, logger: logging.Logger) -> None:
        super().__init__(logger=logger)
        self._connection_string = None
        self._client = None

    @abstractmethod
    def check_availability(self) -> bool:
        """
        Check availability of resource
        """
        raise NotImplementedError
