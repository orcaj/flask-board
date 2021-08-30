from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class QuestionForm(FlaskForm):
    subject = StringField('Title', validators=[DataRequired('title field is required one')])
    content = TextAreaField('content', validators=[DataRequired('content field is required one')])

class AnswerForm(FlaskForm):
    content = TextAreaField('content', validators=[DataRequired('content is required field')])

class UserForm(FlaskForm):
    username=StringField('username', validators=[DataRequired('username is required field'), Length(min=3, max=25)])
    password1=PasswordField('password1', validators=[EqualTo('password2', "Don't matche password"), DataRequired()])
    password2=PasswordField('password2', validators=[DataRequired()])
    email=EmailField('email', validators=[DataRequired(), Email()])

class UserLoginForm(FlaskForm):
    username=StringField('username', validators=[DataRequired('username is required field')])
    password=PasswordField('password', validators=[DataRequired('password is required field')])

class CommentForm(FlaskForm):
    content = TextAreaField('content', validators=[DataRequired()])

