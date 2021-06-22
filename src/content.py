from flask import (
    Blueprint, flash, g, render_template, request, current_app
)

from src.auth import login_required
from src.models import db, BookModel, UserModel, HidingplaceModel
from datetime import date

bp = Blueprint('content', __name__, url_prefix='/content')


@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    """
    this function checks if a user is logged in
    normally no error should be thrown here, but if you know the endpoint...
    :return:
    """
    # g.user is actual logged in user -> see load_logged_in_user
    user = g.user

    try:
        if user is None:
            raise Exception('no user found in database -> cannot happen because user is logged in')
    except Exception as e:
        flash(str(e))
        return render_template('content/error.html')

    # show profile page
    return render_template('content/profile.html', infos=g.user)


@bp.route('/addBook', methods=['GET', 'POST'])
@login_required
def addBook():
    """
    function to add books to the database
    login required -> only for registered users
    :return: addBook page with all user books
    """
    # some variables -> see load_logged_in_user
    user = g.user
    hplaces = g.hidingplaces  # HidingplaceModel -> db query

    # get all user books and hidden user books from database
    ubooks, hubooks = getuserbooks(user.id, hplaces)

    if request.method == 'POST':
        # get input from form
        title = request.form['title']
        bauthor = request.form['bauthor']
        isbn = request.form['isbn']

        error = None

        if not title:
            error = 'Title is required'

        if error is None:
            # here is no check if book is present, a user can add a book more than once
            new_book = BookModel(user.id, title, bauthor, isbn, date=date.today().isoformat())
            db.session.add(new_book)
            db.session.commit()
            flash("New Book added")
            # update books
            ubooks, hubooks = getuserbooks(user.id, hplaces)
            render_template('content/addBook.html', ubooks=ubooks, hubooks=hubooks)

        # display error message
        flash(error)

    # get mode
    return render_template('content/addBook.html', ubooks=ubooks, hubooks=hubooks)


@bp.route('/map', methods=['GET'])
def map():
    """
    function for /map route
    displays the map and shows all hidden books, and i a user is logged in -> shows user position and books
    :return:
    """
    # some variables
    user = g.user

    # query all books and hidingplaces
    hidingplaces = HidingplaceModel.query.all()
    qbooks = BookModel.query.all()

    # get all hidden books
    books = gethiddenbooks(qbooks, hidingplaces)

    # user is logged in -> show all the hidden books and the users hidden books
    if user is not None:
        ubooks, hubooks = getuserbooks(user.id, hidingplaces)

        return render_template('content/map.html', user=user, books=books, ubooks=ubooks,
                               hubooks=hubooks)
    # show only hidden books
    else:
        current_app.logger.info('%s', books)
        return render_template('content/map.html', user=None, books=books, ubooks=None, hubooks=None)


@bp.route('/markbook', methods=['POST'])
def markbook():
    """
    only a post route for getting the json data back
    creates database entry for a hidden book
    :return:
    """
    user = g.user
    if request.method == 'POST':
        # check received data and fill database
        msg = checkhidinglocations(request.get_json())
        flash(msg)


@bp.route('/setownpos', methods=['POST'])
def setownpos():
    """
    only a post route for getting json data back
    updates coordinates for home position of logged in user
    :return:
    """
    user = g.user
    userdata = UserModel.query.filter_by(id=user.id).first()
    data = request.get_json()
    if request.method == 'POST':
        userdata.usercoord = str(data['lat']) + "," + str(data['lng'])
        db.session.add(userdata)
        db.session.commit()
        flash('home coordinates updated')


def gethiddenbooks(qbooks, hidingplaces):
    """
    calculates a dict of all hidden books

    :param qbooks: query object BookModel
    :param hidingplaces: query object HidingplaceModel
    :return: dict
    """
    books = dict()
    # check for tagged books in hidingplaces
    for book in qbooks:
        # if book.id in hidingplace fill data and show the map
        for hidingplace in hidingplaces:
            if book.id == hidingplace.hbook_id:
                books[book.id] = {'title': book.title,
                                  'author': book.author,
                                  'isbn': book.isbn,
                                  'coord': hidingplace.coordinates
                                  }
    return books


def getuserbooks(userid, hidingplaces):
    """
    calculates a dict of all user books and hidden user books
    :param userid: id of current user
    :param hidingplaces: query object of HidingplaceModel
    :return: dict, dict
    """
    # all user books
    qubooks = BookModel.query.filter_by(owner_id=userid).all()
    ubooks = dict()
    # bring it in a good shape
    for book in qubooks:
        ubooks[book.id] = {'title': book.title,
                           'author': book.author,
                           'isbn': book.isbn,
                           }
    # all hidden user books
    hubooks = gethiddenbooks(qubooks, hidingplaces)

    return ubooks, hubooks


def checkhidinglocations(data):
    """
    checks if a book has a hiding place
    creates database entry if no hiding place is present
    returns a flash message
    :param data: request of markbook
    :return: str
    """
    current_app.logger.info('%s', data['user'])

    if data is not None:
        book = HidingplaceModel.query.filter_by(hbook_id=data['book']).all()

        if book is None:
            new_hidingplace = HidingplaceModel(data['user'], data['book'],
                                               str(data['location']['lat']) + "," +
                                               str(data['location']['lng']),
                                               None,
                                               date=date.today().isoformat())
            db.session.add(new_hidingplace)
            db.session.commit()
            return "New hidden book added"
        else:
            return "Book already hidden"
