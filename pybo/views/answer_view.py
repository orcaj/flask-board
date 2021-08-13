from flask import Blueprint, request, url_for, redirect, g, flash, render_template

from pybo.models import Question, Answer

from datetime import datetime

from pybo import db

from ..forms import AnswerForm
from pybo.views.auth import login_required

bp=Blueprint('answer', __name__, url_prefix="/answer")

@bp.route('/create/<int:question_id>', methods=['POST'])
@login_required
def create(question_id):
    form=AnswerForm()
    question=Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content=request.form['content']
        answer=Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.add(answer)
        db.session.commit()
    return redirect(url_for('question.detail', id=question_id))

@bp.route('/modify/<int:answer_id>', methods=['POST', 'GET'])
@login_required
def modify(answer_id):
    answer=Answer.query.get(answer_id)
    form=AnswerForm()
    if g.user != answer.user:
        flash('permisson error')
        return redirect(url_for('question.detail', id=answer.question_id))
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date=datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', id=answer.question_id))
    else:
        form=AnswerForm(obj=answer)
    return render_template('answer/form.html', form=form)

@bp.route('/delete/<int:answer_id>')
def delete(answer_id):
    answer=Answer.query.get(answer_id)
    if answer.user != g.user:
        flash('no permission')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', id=answer.question_id))

