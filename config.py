import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config (object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-guess-it-yes'
    
    # database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'movies.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OMDB API
    OMDB_API_KEY = os.environ.get('OMDB_API_KEY')
    OMDB_URL = os.environ.get('OMDB_URL') 
    # Caching Redis
    CACHE_TYPE = os.environ.get('CACHE_TYPE') or "RedisCache"
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST')  
    CACHE_REDIS_PORT = os.environ.get('CACHE_REDIS_PORT') or 17128
    CACHE_REDIS_PASSWORD = os.environ.get('CACHE_REDIS_PASSWORD') 
    # CACHE_REDIS_USERNAME = os.environ.get('CACHE_REDIS_PASSWORD') or "default"
    CACHE_DEFAULT_TIMEOUT = os.environ.get('CACHE_DEFAULT_TIMEOUT') or 600

    # Caching HomePage
    CACHE_TYPE_WP = 'simple'
    CACHE_DEFAULT_TIMEOUT_WP = 86400


    # Qdrant API
    QDRANT_API_KEY = os.environ.get('QDRANT_KEY') 
    QDRANT_URL = os.environ.get('QDRANT_URL')
    QDRANT_COLLECTION_NAME = os.environ.get('QDRANT_COLLECTION_NAME')