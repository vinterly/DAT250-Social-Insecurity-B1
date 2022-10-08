import os

# contains application-wide configuration, and is loaded in __init__.py


class Config(object):
    DEBUG = False,
    # Secret key should be stored in .env - TODO at some point?
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    DATABASE = 'database.db'
    UPLOAD_FOLDER = 'app/static/uploads'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'gif', 'png'}
    # Restrict uploads to 1 MB
    # Not entirely sure if it works so TODO?
    MAX_CONTENT_LENGTH = 1024 * 1024
