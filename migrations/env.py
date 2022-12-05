from __future__ import with_statement

import logging
from logging.config import fileConfig
from fastapi import FastAPI
import os


from dotenv import dotenv_values
config = {
    **dotenv_values(os.getenv("APP_CONFIG")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

def create_app():
    app = FastAPI(title="xurlpay API alembic")
    return app

# from flask import current_app
# from api import create_app
current_app = create_app()

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
a_config = context.config

# # Interpret the config file for Python logging.
# # This line sets up loggers basically.
# fileConfig(config.config_file_name)
# logger = logging.getLogger('alembic.env')

# # add your model's MetaData object here
# # for 'autogenerate' support
# # from myapp import mymodel
# # target_metadata = mymodel.Base.metadata
# config.set_main_option(
#     'sqlalchemy.url',
#     str(current_app.extensions['migrate'].db.get_engine().url).replace(
#         '%', '%%'))
# target_metadata = current_app.extensions['migrate'].db.metadata

# # other values from the config, defined by the needs of env.py,
# # can be acquired:
# # my_important_option = config.get_main_option("my_important_option")
# # ... etc.


# def run_migrations_offline():
#     """Run migrations in 'offline' mode.

#     This configures the context with just a URL
#     and not an Engine, though an Engine is acceptable
#     here as well.  By skipping the Engine creation
#     we don't even need a DBAPI to be available.

#     Calls to context.execute() here emit the given string to the
#     script output.

#     """
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url, target_metadata=target_metadata, literal_binds=True
#     )

#     with context.begin_transaction():
#         context.run_migrations()


# def run_migrations_online():
#     """Run migrations in 'online' mode.

#     In this scenario we need to create an Engine
#     and associate a connection with the context.

#     """

#     # this callback is used to prevent an auto-migration from being generated
#     # when there are no changes to the schema
#     # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
#     def process_revision_directives(context, revision, directives):
#         if getattr(config.cmd_opts, 'autogenerate', False):
#             script = directives[0]
#             if script.upgrade_ops.is_empty():
#                 directives[:] = []
#                 logger.info('No changes in schema detected.')

#     connectable = current_app.extensions['migrate'].db.get_engine()

#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection,
#             target_metadata=target_metadata,
#             process_revision_directives=process_revision_directives,
#             **current_app.extensions['migrate'].configure_args
#         )

#         with context.begin_transaction():
#             context.run_migrations()


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()

# ---------------- added code here -------------------------#
# this will overwrite the ini-file sqlalchemy.url path
# with the path given in the config of the main code
a_config.set_main_option("sqlalchemy.url", config["DATABASE_URL"])
#------------------------------------------------------------#
# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(a_config.config_file_name)

# ---------------- added code here -------------------------#
from api import models
# #------------------------------------------------------------#
# # ---------------- changed code here -------------------------#
# # here target_metadata was equal to None
target_metadata = models.Base.metadata
# #------------------------------------------------------------#
