from flask import Flask, g, session
from config import Config
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required
import sqlite3
import os

csrf = CSRFProtect()
# create and configure app
app = Flask(__name__)
Bootstrap(app)
csrf.init_app(app)
app.secret_key = g  # &/vg59"#F04&)#
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(Config)


# TODO: Handle login management better, maybe with flask_login?
# TODO: Update the entire app to Flask 2.x at some point? Outdated components.......

@login_manager.user_loader
def load_user(user_id):
    '''conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, [password] from Users where id = (?)",[user_id]) '''
    user_info = query_db(
        'SELECT id, username, [password] FROM Users WHERE id=?;', [user_id], one=True)
    #user_info = cur.fetchone()
    if user_info == None:
        return None
    else:
        return User(int(user_info['id']), user_info['username'], user_info['password'])


login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.authenticated = False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


# get an instance of the db


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # TODO: Missing close?
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

# initialize db for the first time


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# perform generic query, not very secure yet


def query_db(query, args, one=False):
    db = get_db()
    cursor = db.execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    db.commit()
    return (rv[0] if rv else None) if one else rv

# TODO: Add more specific queries to simplify code, and make it more secure

# automatically called when application is closed, and closes db connection


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# initialize db if it does not exist
if not os.path.exists(app.config['DATABASE']):
    init_db()

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])

# NOTE. from app import routes should be at the bottom, otherwise circular import error might occur (design flaw?)
from app import routes