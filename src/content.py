import json

from flask import (
    Blueprint, flash, g, render_template, request, current_app, session
)

from src.auth import login_required
from src.models import db, BookModel, UserModel, HidingplaceModel, LocationModel
from datetime import date
from src.infocollector import InfoCollector

bp = Blueprint('content', __name__, url_prefix='/content')


@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    # g.user is actual logged in user -> see load_logged_in_user
    user = g.user

    try:
        if user is None:
            raise Exception('no user found in database -> cannot happen because user is logged in')
    except Exception as e:
        flash(e)

    return render_template('content/profile.html', infos=g.user)


@bp.route('/addBook', methods=['GET', 'POST'])
@login_required
def addBook():
    user = g.user
    books = g.books

    if request.method == 'POST':
        title = request.form['title']
        bauthor = request.form['bauthor']
        isbn = request.form['isbn']

        error = None

        if not title:
            error = 'Title is required'

        if error is None:
            new_book = BookModel(user.id, title, bauthor, isbn, date=date.today().isoformat())
            db.session.add(new_book)
            db.session.commit()
            flash("New Book added")

        flash(error)

    return render_template('content/addBook.html', books=books)


@bp.route('/map', methods=['GET'])
def map():
    # some variables
    user = g.user
    books = dict()
    allbooks = dict()
    # books = json.dumps(BookModel.query.all())
    # books = InfoCollector(user.id).returnallbooks()

    qbooks = BookModel.query.all()
    qubooks = BookModel.query.filter_by(owner_id=user.id).all()
    hidingplaces = HidingplaceModel.query.all()
    # get list of books for current user
    for book in qubooks:
        books[book.id] = {'title': book.title,
                          'author': book.author,
                          'isbn': book.isbn}
    # check for tagged books in hidingplaces
    for book in qbooks:
        allbooks[book.id] = {'title': book.title,
                             'author': book.author,
                             'isbn': book.isbn}
        for hidingplace in hidingplaces:
            if book.id == hidingplace.hbook_id:
                books[book.id] = book

    current_app.logger.info('%s', qubooks)
    current_app.logger.info('%s', json.dumps(allbooks))
    current_app.logger.info('%s', hidingplaces)

    return render_template('content/map.html', user=user.id, books=qubooks)


@bp.route('/markbook', methods=['POST'])
def markbook():
    user = g.user
    if request.method == 'POST':
        data = request.get_json()
        current_app.logger.info('%s', data)
    return render_template('content/map.html', user=user.id)


@bp.route('/setownpos', methods=['POST'])
def setownpos():
    if request.method == 'POST':
        data = request.get_json()
        current_app.logger.info('%s', data)
    return render_template('content/map.html')
