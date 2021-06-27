from .test_main import addbook, login, client, register
from src.models import BookModel

def test_addBook(client):
    """
    Test addBook function with test data
    :param client:
    :return:
    """

    register(client, 'Test', 'test')
    addbook(client, 1, 'Test-Title', 'Test-Author', 987)
    db_data = BookModel.query.filter_by(title='Test-Title').first()
    # check database for book entry
    assert db_data is not None



