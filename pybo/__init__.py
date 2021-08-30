from flask import Flask, render_template

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import MetaData

from flaskext.markdown import Markdown

# import config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

# db=SQLAlchemy()
migrate=Migrate()


def page_not_found(e):
    return render_template('404.html'), 404

def create_app():
    app=Flask(__name__)

    # app.config.from_object(config)
    app.config.from_envvar('APP_CONFIG_FILE')

    db.init_app(app)

    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


    # migrate.init_app(app, db)
    Markdown(app, extensions=['nl2br','fenced_code'])


    from . import models

    from .views import main_views, question_view, answer_view, auth, comment_view, vote_view

    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_view.bp)
    app.register_blueprint(answer_view.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(comment_view.bp)
    app.register_blueprint(vote_view.bp)

    from .filter import format_datetime
    app.jinja_env.filters['date_time']=format_datetime

    # error manage
    app.register_error_handler(404, page_not_found)
    return app