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
from infra.adapters.database.postgres.postgres_adapter import PostgresAdapter
from infra.adapters.storage.minio_adapter import MinioAdapter
from infra.constants._string import (
    AlembicConstants,
    ApplicationConstants,
    ConfigurationConstants,
    MigrateEngineConstants,
    MinioConstants,
    MongoConstants,
    PostgresConstants,
)
from infra.data.migrations.migration_engine import MigrationEngine
from tornado.httpserver import HTTPServer


@dataclass
class BaseBootstrap(ABC):
    configuration: Dict[Any, Any]
    logger: logging.Logger

    def __init__(self, bootstrap_args: Namespace) -> None:
        self.__post_init__(configuration_args=bootstrap_args)

    def __post_init__(self, configuration_args: Namespace) -> None:  # type: ignore[override]
        self.configuration = self._configuration_initialization(args=configuration_args)
        self.logger = self._logger_initialization()

    def _logger_initialization(self) -> logging.Logger:
        logging.config.dictConfig(self.configuration[ConfigurationConstants.LOGGING])
        return logging.getLogger(name=ApplicationConstants.LOGGER_NAME)

    def _configuration_initialization(self, args: Namespace) -> Dict[Any, Any]:
        return yaml.load(stream=args.config.read(), Loader=yaml.SafeLoader)


@dataclass
class ApplicationBootstrap(BaseBootstrap):
    configuration: Dict[Any, Any]
    logger: logging.Logger
    postgres_adapter: PostgresAdapter
    mongo_adapter: PyMongoAdapter
    minio_adapter: MinioAdapter
    server: Optional[HTTPServer] = None

    def __init__(self, bootstrap_args: Namespace) -> None:
        super().__init__(bootstrap_args=bootstrap_args)
        dotenv.load_dotenv(dotenv.find_dotenv())
        self._postgres_initialization()
        self._mongo_initialization()
        self._minio_initialization()

    def _minio_initialization(self) -> None:
        _host: str = os.environ.get(MinioConstants.ENVVAR_MINIO_HOST)
        _port: int = int(os.environ.get(MinioConstants.ENVVAR_MINIO_PORT))
        _access_key: str = os.environ.get(MinioConstants.ENVVAR_MINIO_ACCESS_KEY)
        _secret_key: str = os.environ.get(MinioConstants.ENVVAR_MINIO_SECRET_KEY)
        _secure: bool = eval(os.environ.get(MinioConstants.ENVVAR_MINIO_SECURE))
        # _bucket: str = os.environ.get(MinioConstants.ENVVAR_MINIO_BUCKET_NAME)

        _server: str = f"{_host}:{_port}"

        _minio_credentials = dict(
            host=_server,
            access_key=_access_key,
            secret_key=_secret_key,
            secure=_secure,
        )
        self.minio_adapter = MinioAdapter(logger=self.logger, **_minio_credentials)
        # _minio_msg = f"MINIO CONNECTIVITY with {_host}"
        # self.logger.info(msg=f"STARTING {_minio_msg}")
        # if self.minio_adapter.get_bucket_policy(name=_bucket):
        #     self.logger.info(
        #         msg=f"SUCCESSFUL {_minio_msg}",
        #     )

        # else:
        #     self.logger.error(
        #         msg=f"FAILED {_minio_msg}",
        #     )

        #     raise ConnectionError(f"Could not connect to the minio storage: {_host}")
        pass

    def _mongo_initialization(self) -> None:
        _host = os.environ.get(MongoConstants.ENVVAR_MONGODB_HOST)
        _username = os.environ.get(MongoConstants.ENVVAR_MONGODB_USERNAME)
        _password = os.environ.get(MongoConstants.ENVVAR_MONGODB_PASSWORD, None)
        _db_name = os.environ.get(MongoConstants.ENVVAR_MONGODB_DATABASE)
        mongo_credentials = dict(
            username=_username, password=_password, host=_host, database_name=_db_name
        )
        self.mongo_adapter = PyMongoAdapter.from_dict(self.logger, **mongo_credentials)
        self.logger.info(
            msg=f"STARTING MONGO DATABASE CONNECTIVITY with {self.mongo_adapter.client}"
        )
        if self.mongo_adapter.check_availability():
            self.logger.info(
                msg=f"MONGO DATABASE CONNECTED to {_host}",
            )
        else:
            self.logger.error(
                msg="MONGO DATABASE CONNECTION FAILED",
            )
            raise ConnectionError(f"Could not connect to the mongo database: {_host}")

    def _postgres_initialization(self) -> None:
        _host = os.environ.get(
            PostgresConstants.ENVVAR_POSTGRES_HOST,
        )
        _username = os.environ.get(PostgresConstants.ENVVAR_POSTGRES_USERNAME)
        _password = os.environ.get(PostgresConstants.ENVVAR_POSTGRES_PASSWORD, None)
        _db_name = os.environ.get(PostgresConstants.ENVVAR_POSTGRES_DATABASE)
        postgres_credentials = dict(
            username=_username, password=_password, host=_host, database_name=_db_name
        )
        self.postgres_adapter = PostgresAdapter.from_dict(
            logger=self.logger, **postgres_credentials
        )
        _msg = f"STARTING POSTGRES CONNECTIVITY with {self.postgres_adapter.engine}"
        self.logger.info(msg=_msg)
        if self.postgres_adapter.check_availability():
            self.logger.info(
                msg=f"POSTGRES CONNECTED to {_host}",
            )
            apply_migrations = bool(
                os.environ.get(AlembicConstants.ENVVAR_APPLY_MIGRATIONS_NAME)
            )
            migration_config_file = MigrateEngineConstants.MIGRATION_CONFIG_FILE
            MigrationEngine.migrateapply_migrations(
                logger=self.logger,
                db_engine=self.postgres_adapter.engine,
                config_file=migration_config_file,
                apply_migrations=apply_migrations,
            )

        else:
            self.logger.error(
                msg="POSTGRES DATABASE CONNECTION FAILED",
            )

            raise ConnectionError(
                f"Could not connect to the postgres database: {_host}"
            )
