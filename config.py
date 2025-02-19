import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config (object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-guess-it'
    
    # database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'movies.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OMDB API
    OMDB_API_KEY = os.environ.get('OMDB_API_KEY') or "28c6a732"
    OMDB_URL = os.environ.get('OMDB_URL') or "http://www.omdbapi.com/"

    # Caching Redis
    CACHE_TYPE = os.environ.get('CACHE_TYPE') or "RedisCache"
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST') or "redis-17128.crce182.ap-south-1-1.ec2.redns.redis-cloud.com"
    CACHE_REDIS_PORT = os.environ.get('CACHE_REDIS_PORT') or 17128
    CACHE_REDIS_PASSWORD = os.environ.get('CACHE_REDIS_PASSWORD') or "N7KCwAsyZfeZlcTHWtyLIBDaMl3DMTs9"
    # CACHE_REDIS_USERNAME = os.environ.get('CACHE_REDIS_PASSWORD') or "default"
    CACHE_DEFAULT_TIMEOUT = os.environ.get('CACHE_DEFAULT_TIMEOUT') or 600

    # Caching HomePage
    CACHE_TYPE_WP = 'simple'
    CACHE_DEFAULT_TIMEOUT_WP = 86400


    # Qdrant API
    QDRANT_API_KEY = os.environ.get('QDRANT_KEY') or "R0sgiW6pakm1ZnSqy7oWVYEhbzXpT1EUCQ16GoSNVKmjyV-oyLU2XQ"
    QDRANT_URL = os.environ.get('QDRANT_URL') or "https://5c4686a7-f60e-445b-81c2-b235697b9d42.europe-west3-0.gcp.cloud.qdrant.io:6333"
    QDRANT_COLLECTION_NAME = os.environ.get('QDRANT_COLLECTION_NAME') or 'recommendation'