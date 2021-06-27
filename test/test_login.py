from .test_main import register, login, client


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