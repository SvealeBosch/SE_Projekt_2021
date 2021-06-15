from src.models import UserModel, BookModel, LocationModel, HidingplaceModel
from flask import g, json, jsonify, current_app


class InfoCollector:
    _instance = None

    @classmethod
    def reset(cls) -> None:
        """
        Resets the current instance
        """
        cls._instance = None

    @classmethod
    def instance(cls) -> 'InfoCollector':
        """
        Resets the current instance
        """
        return cls._instance

    def __new__(cls):
        # if there is no instance yet
        if not cls._instance:
            # instantiate
            cls._instance = super().__new__(cls)
            cls._instance.__init_singleton__()

        return cls._instance

    def __init_singleton__(self, userid) -> None:
        self._allBooks = None
        self._allLocations = None
        self._userid = userid

    def returnallbooks(self):
        res_dict = dict()
        hidingplaces = HidingplaceModel.query.all()

        for hidingplace in hidingplaces:
            book = BookModel.query.filter_by(id=hidingplace.hbook_id)
            location = LocationModel.query.filter_by(id=hidingplace.hlocation_id)
            res_dict[hidingplace.id] = [book.title, book.author, book.isbn, location.coordinates]


    def returnallbooksforuser(self):
        pass
