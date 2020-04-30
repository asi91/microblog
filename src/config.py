import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard-to-guess-secret-key"
    default_db_url = f"sqlite:///{os.path.join(basedir, 'app.db')}"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or default_db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
