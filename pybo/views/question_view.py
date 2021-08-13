from flask import Blueprint, render_template, request, redirect, url_for, g, flash
from pybo.models import Question, Answer

from ..forms import QuestionForm, AnswerForm

from datetime import datetime

from pybo import db
from pybo.views.auth import login_required

bp=Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list')
def _list():
    # pagination
    page = request.args.get('page', type=int, default=1)
    question_list=Question.query.order_by(Question.create_date.desc())
    question_list=question_list.paginate(page, per_page=10)
    return render_template('question/question.html', question_list=question_list)

@bp.route('/detail/<int:id>')
def detail(id):
    form=AnswerForm()
    question=Question.query.get_or_404(id)
    return render_template('question/detail.html', question=question, form=form)

@bp.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    form=QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question=Question(subject = form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/create.html', form=form)

@bp.route('/modify/<int:question_id>', methods=['GET', 'POST'])
def modify(question_id):
    question=Question.query.get_or_404(question_id)
    if question.user != g.user:
        flash('not permission')
        return redirect(url_for('question.detail', id=question_id))
    if request.method == 'POST':
        form=QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date=datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', id=question_id))
    else:
        form=QuestionForm(obj=question)
    return render_template('question/create.html', form=form)

@bp.route('/delete/<int:question_id>')
def delete(question_id):
    question=Question.query.get(question_id)
    if question.user != g.user:
        flash('no permiosson')
        return redirect(url_for('question.detail', id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))