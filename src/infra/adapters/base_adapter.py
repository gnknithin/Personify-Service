import logging
from abc import ABC


class BaseAdapter(ABC):
    '''
    Base Adapter for resources
    '''

    def __init__(
        self,
        logger: logging.Logger,
    ) -> None:
        super().__init__()
        self._logger = logger
