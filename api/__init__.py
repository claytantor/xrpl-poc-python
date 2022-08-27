
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import g
import os
import json
import logging
# from . import models
# from . import routes

from dotenv import dotenv_values
config = {
    **dotenv_values(os.getenv("APP_CONFIG")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

db = SQLAlchemy()

def create_app():

    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    print(json.dumps(config, indent=4))

    app.config.update(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_POOL_SIZE'] = 20
    # app.config["SQLALCHEMY_POOL_TIMEOUT"] = 3600

    # this should be done in the config file
    lookup= {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARN':logging.WARN,
    }
    logging.basicConfig(level=lookup[app.config["APP_LOG_LEVEL"]])


    app.logger.info(f"=== create_app {__name__} ===")
    app.logger.info(json.dumps(config, indent=4))


    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)
    

    with app.app_context():

        from . import routes  # Import routes
        from . import models

        app.logger.info('app setup successfully.')
        
    return app