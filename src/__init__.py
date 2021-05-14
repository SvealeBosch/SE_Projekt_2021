import os
from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # 'dev' to provide a convenient value during development, but it should be overridden with a random value
        # when deploying
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'src.postgresql'),
    )

    # if test_config is None:
    #     # load instance config, if it exists when not testing
    #     app.config.from_mapping('config.py', silent=True)
    # else:
    #     # load test config
    #     app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple hello page
    @app.route('/')
    def hello_world():
        return render_template('index.html')

    return app
