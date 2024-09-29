import logging.config
from abc import ABC
from dataclasses import dataclass

from infrastructure.constants._string import ApplicationConstants
from infrastructure.logging.config import PERSONIFY_LOGGER_CONFIG


@dataclass(
    init=False,
    repr=True,
    eq=True,
    order=True,
    unsafe_hash=False,
    frozen=False,
    match_args=False,
    kw_only=False,
    slots=False,
    weakref_slot=False,
)
class AbstractBootstrap(ABC):
    logger: logging.Logger

    def __init__(self) -> None:
        self.__post_init__()
        super().__init__()

    def __post_init__(self) -> None:
        self.logger = self._logger_initialization()

    def _logger_initialization(self) -> logging.Logger:
        logging.config.dictConfig(config=PERSONIFY_LOGGER_CONFIG)
        return logging.getLogger(name=ApplicationConstants.LOGGER_NAME)
