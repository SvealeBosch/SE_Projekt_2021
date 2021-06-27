from .test_main import register, login, client
from src.models import UserModel


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
    assert b'Bad Request' in rv.data

    rv = register(client, 'Test', None)
    assert b'Bad Request' in rv.data