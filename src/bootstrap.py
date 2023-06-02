import logging
import logging.config
import os
from abc import ABC
from argparse import Namespace
from dataclasses import dataclass
from typing import Any, Dict, Optional

import dotenv
import yaml
from infra.adapters.database.mongo.pymongo_adapter import PyMongoAdapter
from infra.constants._string import (
    ApplicationConstants,
    ConfigurationConstants,
    MongoConstants,
)
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
    configuration: Dict[Any, Any]
    logger: logging.Logger
    mongo_adapter: PyMongoAdapter
    server: Optional[HTTPServer] = None

    def __init__(self, bootstrap_args: Namespace) -> None:
        super().__init__(bootstrap_args=bootstrap_args)
        self._mongo_initialization()

    def _mongo_initialization(self) -> None:
        dotenv.load_dotenv(dotenv.find_dotenv())
        _host = os.environ.get(
            MongoConstants.ENVVAR_MONGODB_HOST
        )
        _username = os.environ.get(
            MongoConstants.ENVVAR_MONGODB_USERNAME
        )
        _password = os.environ.get(
            MongoConstants.ENVVAR_MONGODB_PASSWORD, None
        )
        _db_name = os.environ.get(
            MongoConstants.ENVVAR_MONGODB_DATABASE
        )
        mongo_credentials = dict(
            username=_username,
            password=_password,
            host=_host,
            db_name=_db_name
        )
        self.mongo_adapter = PyMongoAdapter.from_dict(
            self.logger,
            **mongo_credentials
        )
        self.logger.info(
            msg=f'STARTING MONGO DATABASE CONNECTIVITY with {self.mongo_adapter.client}'
        )
        if self.mongo_adapter.check_availability():
            self.logger.info(
                msg=f'MONGO DATABASE CONNECTED to {_host}',
            )
        else:
            self.logger.error(
                msg='MONGO DATABASE CONNECTION FAILED',
            )
            raise ConnectionError(
                f'Could not connect to the mongo database: {_host}'
            )
