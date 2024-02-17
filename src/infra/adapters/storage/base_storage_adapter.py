import logging

from infra.adapters.base_adapter import BaseAdapter


class BaseStorageAdapter(BaseAdapter):
    def __init__(self, logger: logging.Logger) -> None:
        super().__init__(logger=logger)
        self._client = None
