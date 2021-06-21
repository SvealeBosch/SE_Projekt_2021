import pytest

from main import app
from src.models import db, UserModel
from src import config
import logging


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


def test_register(client):
    """
    Test register function with username and password
    :param client:
    :return:
    """

    register(client, 'Test', 'test')
    db_data = UserModel.query.filter_by(username='Test').first()
    # check database for user entry
    assert db_data is not None


def test_register_userpresent(client):
    """
    Test register function with present user
    :param client:
    :return:
    """
    register(client, 'Test', 'test')
    # now the user should be present in database
    rv = register(client, 'Test', 'test')
    assert b'User is already present' in rv.data


def test_register_wronginput(client):
    """
    Test register function without given user name
    :param client:
    :return:
    """

    rv = register(client, None, 'test')
    logging.info('%s', rv.data)
    assert b'Bad Request' in rv.data

    rv = register(client, 'Test', None)
    logging.info('%s', rv.data)
    assert b'Bad Request' in rv.data


def test_login(client):
    """
    Test login function
    :param client:
    :return:
    """
    # register Test user
    register(client, 'Test', 'test')
    rv = login(client, 'Test', 'test')
    assert b'Hello Test' in rv.data


def test_login_wronginput(client):
    """
    Test login function with wrong input
    :param client:
    :return:
    """
    register(client, 'Test', 'test') # precondition
    rv = login(client, 'Test', 'test1') # action -> input, rv -> ausgabe
    assert b'Incorrect username or password' in rv.data # assertion

    rv = login(client, 'Test1', 'test')
    assert b'Incorrect username or password' in rv.data


def test_logout(client):
    """
    Test logout
    :param client:
    :return:
    """
    # register Test user
    register(client, 'Test', 'test')
    login(client, 'Test', 'test')
    rv = logout(client)
    assert b'Test logged out' in rv.data
