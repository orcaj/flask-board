from flask import Blueprint, render_template, url_for, redirect
from pybo.models import Question, Answer

bp=Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello():
    return 'hello'

@bp.route('/')
def index():
    return redirect(url_for('question._list'))