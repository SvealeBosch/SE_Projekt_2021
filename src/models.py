# https://docs.sqlalchemy.org/en/14/core/type_basics.html
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/ -> relations

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# only for command line stuff?
# activate virtual environment and type 'from src.models import db'
# db.create_all() -> creates all tables
# db.drop_all() -> drops all tables
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbuser:YL6%E$xAXL%7Nf4N8&PC@localhost:5432/seprojekt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)  # primary_key -> autoincrement default?
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    name = db.Column(db.String)
    city = db.Column(db.String)
    registered = db.Column(db.DateTime)

    def __init__(self, username, password, email=None, name=None, city=None, registered=None):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.city = city
        self.registered = registered

    def __repr__(self):
        return f"statement"


class BookModel(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    isbn = db.Column(db.String)
    genre = db.Column(db.String)
    language = db.Column(db.String)
    for_age = db.Column(db.String)
    tags = db.Column(db.String)
    publisher = db.Column(db.String)
    condition = db.Column(db.String)
    date = db.Column(db.Date)

    def __init__(self, title, author, isbn, genre, language, for_age, tags, publisher, condition, date):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.language = language
        self.for_age = for_age
        self.tags = tags
        self.publisher = publisher
        self.condition = condition
        self.date = date

    def __repr__(self):
        return f"statement"


class LocationModel(db.Model):
    __tablename__ = 'locations'

    location_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String)
    number = db.Column(db.Integer)
    postcode = db.Column(db.String(5))
    city = db.Column(db.String)
    coordinates = db.Column(db.String)

    def __init__(self, street, number, postcode, city, coordinates):
        self.street = street
        self.number = number
        self.postcode = postcode
        self.city = city
        self.coordinates = coordinates

    def __repr__(self):
        return f"statement"


class HidingplaceModel(db.Model):
    __tablename__ = 'hidingplaces'

    place_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    users = db.relationship("UserModel", backref=db.backref('users', lazy=True))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    books = db.relationship("BookModel", backref=db.backref('books', lazy=True))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
    locations = db.relationship("LocationModel", backref=db.backref('locations', lazy=True))
    notes = db.Column(db.String)
    date = db.Column(db.Date)

    def __init__(self, user_id, book_id, locations_id, notes, date):
        self.user_id = user_id
        self.book_id = book_id
        self.location_id = locations_id
        self.notes = notes
        self.date = date

    def __repr__(self):
        return f"statement"
