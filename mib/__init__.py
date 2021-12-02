"""
Flask initialization
"""
import os

__version__ = "0.1"

import logging
from datetime import timedelta

from celery.schedules import crontab  # cronetab for lottery
from flask import Flask
from flask_environments import Environments

debug_toolbar = None
redis_client = None
app = None
api_app = None
logger = None


def create_app():
    """
    This method create the Flask application.
    :return: Flask App Object
    """
    global app
    global api_app

    # first initialize the logger
    init_logger()

    # getting the flask app
    app = Flask(__name__)

    flask_env = os.getenv("FLASK_ENV", "None")
    if flask_env == "development":
        config_object = "config.DevConfig"
    elif flask_env == "testing":
        config_object = "config.TestConfig"
    elif flask_env == "production":  # pragma: no cover
        config_object = "config.ProdConfig"
    else:
        raise RuntimeError(  # pragma: no cover
            "%s is not recognized as valid app environment. You have to setup the environment!"
            % flask_env
        )

    # Load config
    env = Environments(app)
    env.from_object(config_object)

    return app


def init_logger():
    global logger
    """
    Initialize the internal application logger.
    :return: None
    """
    logger = logging.getLogger(__name__)
    from flask.logging import default_handler

    logger.addHandler(default_handler)
