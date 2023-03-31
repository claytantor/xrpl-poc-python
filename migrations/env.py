from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context as alembic_context


import os

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("APP CONFIG PATH: " + os.getenv("APP_CONFIG"))

from dotenv import dotenv_values
e_config = {
    **dotenv_values(os.getenv("APP_CONFIG")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
a_config = alembic_context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if a_config.config_file_name is not None:
    fileConfig(a_config.config_file_name)

a_config.set_main_option("sqlalchemy.url", e_config["DATABASE_URL"])

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# ---------------- added code here -------------------------#
import api.models
#------------------------------------------------------------#
# ---------------- changed code here -------------------------#
# here target_metadata was equal to None
target_metadata = api.models.Base.metadata
#------------------------------------------------------------#


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = a_config.get_main_option("sqlalchemy.url")
    alembic_context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with alembic_context.begin_transaction():
        alembic_context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        a_config.get_section(a_config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        alembic_context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with alembic_context.begin_transaction():
            alembic_context.run_migrations()


if alembic_context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
