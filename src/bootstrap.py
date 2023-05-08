import logging
import logging.config
from abc import ABC
from argparse import Namespace
from dataclasses import dataclass
from typing import Any, Dict, Optional

import yaml
from infra.constants._string import ApplicationConstants, ConfigurationConstants
from tornado.httpserver import HTTPServer


@dataclass
class BaseBootstrap(ABC):
    configuration: Dict[Any, Any]
    logger: logging.Logger

    def __init__(self, bootstrap_args: Namespace) -> None:
        self.__post_init__(
            configuration_args=bootstrap_args
        )

    def __post_init__(self, configuration_args: Namespace) -> None:
        self.configuration = self._configuration_initialization(
            args=configuration_args
        )
        self.logger = self._logger_initialization()

    def _logger_initialization(self) -> logging.Logger:
        logging.config.dictConfig(
            self.configuration[ConfigurationConstants.LOGGING]
        )
        return logging.getLogger(ApplicationConstants.LOGGER_NAME)

    def _configuration_initialization(self, args: Namespace) -> Dict[Any, Any]:
        return yaml.load(args.config.read(), Loader=yaml.SafeLoader)


@dataclass
class ApplicationBootstrap(BaseBootstrap):
    configuration : Dict[Any,Any]
    logger: logging.Logger
    server: Optional[HTTPServer] = None

    def __init__(self, bootstrap_args: Namespace) -> None:
        super().__init__(bootstrap_args=bootstrap_args)
