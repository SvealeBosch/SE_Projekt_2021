import pytest

from main import app
from src.models import db
from src import config
from unittest.mock import MagicMock


@pytest.fixture
def client():
    """
    client application which starts flask with TestingConfig
    prepares database for testing
    :return:
    """
    app.config.from_object(config.Config)
    app.config.from_object(config.TestingConfig)

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.init_app(app)
        yield client


def login(client, username, password):
    """
    wrapper for login function
    :param client: test application
    :param username: test username
    :param password: test password
    :return: response of post request
    """
    return client.post('/auth/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    """
    wrapper for logout function
    :param client: test application
    :return: response of get request
    """
    return client.get('auth/logout', follow_redirects=True)


def register(client, username, password):
    """
    wrapper to register function
    :param client: test application
    :param username: test username
    :param password: test password
    :return: response of post request
    """
    return client.post('/auth/register', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def addbook(client, userid, title, author, isbn):
    """
    :param client:
    :param userid:
    :param title:
    :param bauthor:
    :param isbn:
    :return:
    """

    from src.content import getuserbooks
    getuserbooks = MagicMock(return_value="dummy")

    return client.post('/content/addBook', data=dict(
        user=None,
        hplaces=None,
        ubooks=None,
        hubooks=None,
        userid=userid,
        title=title,
        bauthor=author,
        isbn=isbn
    ), follow_redirects=True)
