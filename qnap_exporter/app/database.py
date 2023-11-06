from flask_sqlalchemy import SQLAlchemy
from flask import g


# https://stackoverflow.com/questions/32922210/why-does-a-query-invoke-a-auto-flush-in-sqlalchemy
SESSION_OPTIONS = {"autoflush": False}


def get_db():
    if 'db' not in g:
        g.db = SQLAlchemy(session_options=SESSION_OPTIONS)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.session.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    db = get_db()
    db.init_app(app)
    return db


class DBSessionWrapper(object):
    def __init__(self, session):
        self.session = session
