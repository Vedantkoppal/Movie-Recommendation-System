import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config (object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-guess-it'
    
    # database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'movies.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OMDB API
    OMDB_API_KEY = os.environ.get('OMDB_API_KEY') or ""
    OMDB_URL = os.environ.get('OMDB_URL') or ""

    # Caching settings
    CACHE_TYPE = "simple"
