# https://docs.sqlalchemy.org/en/14/core/type_basics.html
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/ -> relations

# Sources
# https://wakatime.com/blog/32-flask-part-1-sqlalchemy-models-to-json -> serialization method

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

# Serialization method: Returns models as dictionary - See Source above
class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self, show=None, _hide=[], _path=None):
        """Return a dictionary representation of this model."""

        show = show or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else []
        default.extend(['id', 'modified_at', 'created_at'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class
                        is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide),
                        _path=("%s.%s" % (_path, key.lower())),
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data


class UserModel(BaseModel):
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


class BookModel(BaseModel):
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


class LocationModel(BaseModel):
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


class HidingplaceModel(BaseModel):
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



