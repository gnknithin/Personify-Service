import logging

from alembic import command
from alembic.config import Config
from infra.constants._string import MigrateEngineConstants
from sqlalchemy.engine import Engine


class MigrationEngine:
    def __init__(
        self,
        logger: logging.Logger,
        db_engine: Engine,
        config_file: str,
        apply_migrations: bool
    ):
        self._logger = logger
        self._db_engine = db_engine
        self._apply_migrations = apply_migrations

        self._alembic_config = Config(config_file)

    @classmethod
    def migrateapply_migrations(
        cls,
        logger: logging.Logger,
        db_engine: Engine,
        config_file: str,
        apply_migrations: bool
    ):
        migration_engine = cls(
            logger=logger,
            db_engine=db_engine,
            config_file=config_file,
            apply_migrations=apply_migrations
        )

        migration_engine.migrate()

    def migrate(self):
        if self._apply_migrations:
            self._logger.info(
                msg=f'Applying DB migrations on {self._db_engine} if is needed'
            )

            with self._db_engine.begin() as connection:
                self._alembic_config.attributes[
                    MigrateEngineConstants.CONNECTION
                ] = connection
                command.upgrade(
                    self._alembic_config,
                    MigrateEngineConstants.HEAD
                )

            self._logger.info(
                msg='DB migrations applied'
            )
        else:
            self._logger.info(
                msg='Skipped DB migrations'
            )
