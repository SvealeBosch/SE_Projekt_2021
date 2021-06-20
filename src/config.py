import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    main class for configuration
    """
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
    """
    class for production configuration
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://dbuser:YL6%E$xAXL%7Nf4N8&PC@localhost:5432/produktivdb"


class StagingConfig(Config):
    """
    class for staging configuration
    not necessary now
    """
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """
    class for development configuration
    """
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://dbuser:YL6%E$xAXL%7Nf4N8&PC@localhost:5432/seprojekt"


class TestingConfig(Config):
    """
    class for testing configuration
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://dbuser:YL6%E$xAXL%7Nf4N8&PC@localhost:5432/projtestdb"