import os
from flask import Flask, render_template, jsonify, request
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from src import config
from src.models import db, UserModel
import json

db = SQLAlchemy()


def create_app(test_config=None):
    """
    creates flask application and initializes database
    :param test_config:
    :return: app
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.Config)

    # activate when testing
    if test_config is None:
        # load instance config, if it exists when not testing
        app.config.from_object(config.DevelopmentConfig)
    else:
        # load test config
        app.config.from_object(config.TestingConfig)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize db
    db.init_app(app)

    # routes to the sub-pages -> every html page needs one or the navigation won't work
    @app.route('/')
    def mainpage():
        return render_template('content/index.html')

    from . import auth
    # registers entry point auth
    app.register_blueprint(auth.bp)

    from . import content
    # registers entry point auth content
    app.register_blueprint(content.bp)

    return app
