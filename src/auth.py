import functools
import logging

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from src.models import db, UserModel, BookModel

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = 'User is already present, please choose another username'

        if error is None:
            new_user = UserModel(username, password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']

        error = None
        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username or password.'
        elif not check_password_hash(user.password, request.form['password']):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('content/index'))

        flash(error)
    return render_template('auth/login.html')


# called before every request
# g is a special variable -> lasts for one request
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = UserModel.query.filter_by(id=user_id).first()
        g.books = BookModel.query.filter_by(owner_id=user_id).all()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('content/index'))


# wrapper for content
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
