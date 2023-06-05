from logging.config import fileConfig

from alembic import context
from bootstrap import ApplicationBootstrap
from domain.user_model import UserModel
from infra.constants._string import MigrateEngineConstants
from infra.parser.argument_parser import ArgumentParser

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# CUSTOM-MODIFICATION
if config.config_file_name is not None:
    try:
        fileConfig(config.config_file_name)
    except KeyError:
        pass

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# CUSTOM-MODIFICATION
target_metadata = [UserModel.metadata]

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_bootstrap():
    # CUSTOM-MODIFICATION
    args = ['--config', './configs/development.yaml']
    return ApplicationBootstrap(
        bootstrap_args=ArgumentParser.parse_arguments(args)
    )


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # CUSTOM-MODIFICATION
    try:
        connectable = config.attributes.get(
            MigrateEngineConstants.CONNECTION, None
        )
    except AttributeError:
        connectable = None

    if connectable is None:
        _boostrap = get_bootstrap()
        connectable = _boostrap.postgres_adapter.engine

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata
            )

            with context.begin_transaction():
                context.run_migrations()
    else:
        context.configure(
            connection=connectable,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
