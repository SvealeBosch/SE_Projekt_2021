import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle': 60,
                                 'max_overflow': -1,
                                 'pool_size': 20,
                                 'pool_timeout': 30
                                 }


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://dbuser:YL6%E$xAXL%7Nf4N8&PC@localhost:5432/projektdb"


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://dbuser:YL6%E$xAXL%7Nf4N8&PC@localhost:5432/seprojekt"


class TestingConfig(Config):
    TESTING = True
