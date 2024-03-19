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
from infra.adapters.storage.minio_admin_adapter import MinIOAdminAdapter
from infra.adapters.storage.minio_app_user_adapter import MinIOAppUserAdapter
from infra.adapters.storage.minio_root_adapter import MinIORootAdapter
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
    minio_admin_adapter: MinIOAdminAdapter
    minio_root_adapter: MinIORootAdapter
    minio_app_user_adapter: MinIOAppUserAdapter
    server: Optional[HTTPServer] = None

    def __init__(self, bootstrap_args: Namespace) -> None:
        super().__init__(bootstrap_args=bootstrap_args)
        _ = dotenv.load_dotenv(dotenv.find_dotenv())
        self._postgres_initialization()
        self._mongo_initialization()
        self._minio_initialization()

    def _minio_initialization(self) -> None:
        _host: str = os.environ.get(MinioConstants.ENVVAR_MINIO_HOST, "")
        _port: int = int(os.environ.get(MinioConstants.ENVVAR_MINIO_PORT, 9000))
        _access_key: str = os.environ.get(MinioConstants.ENVVAR_MINIO_ACCESS_KEY, "")
        _secret_key: str = os.environ.get(MinioConstants.ENVVAR_MINIO_SECRET_KEY, "")
        _secure: bool = (
            True
            if (os.environ.get(MinioConstants.ENVVAR_MINIO_SECURE, "True") == "True")
            else False
        )

        _app_user_access_key: str = os.environ.get(
            MinioConstants.ENVVAR_MINIO_APP_USER_ACCESS_KEY, ""
        )
        _app_user_secret_key: str = os.environ.get(
            MinioConstants.ENVVAR_MINIO_APP_USER_SECRET_KEY, ""
        )
        _app_bucket: str = os.environ.get(MinioConstants.ENVVAR_MINIO_BUCKET_NAME, "")

        _server: str = f"{_host}:{_port}"

        _minio_root_credentials = dict(
            host=_server,
            access_key=_access_key,
            secret_key=_secret_key,
            secure=_secure,
        )
        _minio_app_user_credentials = dict(
            host=_server,
            access_key=_app_user_access_key,
            secret_key=_app_user_secret_key,
            secure=_secure,
        )
        self.minio_admin_adapter = MinIOAdminAdapter(
            logger=self.logger, **_minio_root_credentials
        )
        _minio_msg = f"MINIO CONNECTIVITY with {_host}"
        self.logger.info(msg=f"STARTING {_minio_msg}")
        # STEP-01 Check MINIO Availability
        if self.minio_admin_adapter.check_avilability():
            self.logger.info(
                msg=f"SUCCESSFUL {_minio_msg}",
            )
            # STEP-02 Initialize Root Adapter
            self.minio_root_adapter = MinIORootAdapter(
                logger=self.logger, **_minio_root_credentials
            )
            # STEP-03 Check App Bucket Exists
            if self.minio_root_adapter.bucket_exists(bucket_name=_app_bucket) is False:
                # TODO STEP-03 Create App Bucket
                _created_app_bucket = self.minio_root_adapter.create_bucket(
                    bucket_name=_app_bucket
                )
                assert _created_app_bucket is None
            # STEP-04 Check AppUser Exists
            if (
                self.minio_admin_adapter.check_user_exists(
                    user_access_key=_app_user_access_key
                )
                is False
            ):
                _created_app_user = self.minio_admin_adapter.add_user(
                    user_access_key=_app_user_access_key,
                    user_secret_key=_app_user_secret_key,
                )
                assert _created_app_user is not None
            # Step-04 Initialize MinIOAppUserAdapter using APPUSER to limit ROOT permissions
            self.minio_app_user_adapter = MinIOAppUserAdapter(
                logger=self.logger, **_minio_app_user_credentials
            )
            # TODO Check PersonifyAppUserGroup Exists OR Create PersonifyAppUserGroup and add Policy to it
            # TODO Check PersonifyAppUserPolicy Exists OR Create PersonifyAppUserPolicy
            # Check Bucket Policy and Update According to REQUIREMENT
            # https://min.io/docs/minio/container/administration/identity-access-management/policy-based-access-control.html#policy-document-structure
        else:
            self.logger.error(
                msg=f"FAILED {_minio_msg}",
            )

            raise ConnectionError(f"Could not connect to the minio storage: {_host}")

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
