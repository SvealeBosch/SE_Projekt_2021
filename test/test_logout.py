from .test_main import register, login, client, logout


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