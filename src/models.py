# https://docs.sqlalchemy.org/en/14/core/type_basics.html
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/ -> relations

# Sources
# https://wakatime.com/blog/32-flask-part-1-sqlalchemy-models-to-json -> serialization method
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# only for command line stuff?
# activate virtual environment and type 'from src.models import db'
# db.create_all() -> creates all tables
# db.drop_all() -> drops all tables
from sqlalchemy.orm.attributes import QueryableAttribute

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbuser:YL6%E$xAXL%7Nf4N8&PC@localhost:5432/seprojekt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class UserModel(db.Model):
    """
    model class for db table users with given columns
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # primary_key -> autoincrement default?
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    name = db.Column(db.String)
    city = db.Column(db.String)
    usercoord = db.Column(db.String)
    registered = db.Column(db.DateTime)

    def __init__(self, username, password, email=None, name=None, city=None, usercoord=None, registered=None):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.city = city
        self.usercoord = usercoord
        self.registered = registered

    def __repr__(self):
        return json.dumps({'username': self.username,
                           'password': self.password,
                           'email': self.email,
                           'name': self.name,
                           'city': self.city,
                           'usercoord': self.usercoord,
                           'registered': self.registered})


class BookModel(db.Model):
    """
    model class for db table books with given columns
    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
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

    def __init__(self, owner_id, title, author, isbn, genre=None, language=None, for_age=None, tags=None,
                 publisher=None, condition=None, date=None):
        self.owner_id = owner_id
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
        return json.dumps({'title': self.title,
                           'author': self.author,
                           'isbn': self.isbn})


class HidingplaceModel(db.Model):
    """
    model class for db table hidingplaces with given columns
    """
    __tablename__ = 'hidingplaces'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    hbook_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    coordinates = db.Column(db.String)
    notes = db.Column(db.String)
    date = db.Column(db.Date)

    def __init__(self, owner_id, hbook_id, coordinates, notes, date):
        self.owner_id = owner_id
        self.hbook_id = hbook_id
        self.coordinates = coordinates
        self.notes = notes
        self.date = date

    def __repr__(self):
        return json.dumps({'owner_id': self.owner_id,
                           'hbook_id': self.hbook_id,
                           'coordinates': self.coordinates,
                           'notes': self.notes,
                           'date': self.date})
