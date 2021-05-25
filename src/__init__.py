import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from src import config
from src.models import db

db = SQLAlchemy()

def create_app(test_config=None):
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

    @app.route('/map')
    def map():
        return render_template('content/map.html')

    @app.route('/login')
    def login():
        return render_template('auth/login.html')

    from . import auth
    app.register_blueprint(auth.bp)

    from . import content
    app.register_blueprint(content.bp)
    app.add_url_rule('/', endpoint='content/index')

    return app
