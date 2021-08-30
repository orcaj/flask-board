from flask import Blueprint, flash, g, redirect, url_for

from pybo import db
from pybo.models import Question, Answer

from pybo.views.auth import login_required

bp=Blueprint('vote', __name__, url_prefix='/vote')

@bp.route('/vote/question/<int:question_id>/')
@login_required
def question(question_id):
    _question=Question.query.get_or_404(question_id)
    if g.user==_question.user:
        flash("you can't vote your question")
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', id=_question.id))

@bp.route('/answer/vote/<int:answer_id>')
@login_required
def answer(answer_id):
    _answer=Answer.query.get_or_404(answer_id)
    if g.user == _answer.user:
        flash('you can\'t vote your answer')
    else:
        _answer.voter.append(g.user)
        db.session.commit()
    return redirect('{}#answer_{}'.format(url_for('question.detail', id=_answer.question.id), _answer.id))