from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from ..forms import UserForm, UserLoginForm
from pybo.models import User

from pybo import db
import functools

bp=Blueprint('auth', __name__, url_prefix="/auth")

@bp.route('/signup', methods=['POST', 'GET'])
def signup():
    form=UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            flash("this user is already exit")
        else:
            user=User(username=form.username.data, password=generate_password_hash(form.password1.data), email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
    return render_template('auth/signup.html', form=form)

@bp.route('/login', methods=['POST', 'GET'])
def login():
    form=UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error=None
        user=User.query.filter_by(username=form.username.data).first()
        if not user:
            error="Don't exist user"

        elif not check_password_hash(user.password, form.password.data):
            error="Password isn't correct"

        if error is None:
            session.clear()
            session['user_id']=user.id
            return redirect(url_for('main.index'))
        flash(error)

    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id=session.get('user_id')
    if user_id:
        user=User.query.get(user_id)
        g.user=user
    else:
        g.user=None

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


