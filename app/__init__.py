from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
# from flask_caching import Cache


from qdrant_client import QdrantClient
import redis


app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
socketio = SocketIO(app)

# cache = Cache(app)


try:
    redis_client = redis.StrictRedis(
        host=app.config['CACHE_REDIS_HOST'],
        port=app.config['CACHE_REDIS_PORT'],
        username = app.config['CACHE_REDIS_USERNAME'],
        password=app.config['CACHE_REDIS_PASSWORD'],
        decode_responses=True,
        socket_timeout=5,  # Timeout for Redis operations (in seconds)
        socket_connect_timeout=3,  # Timeout for connecting to Redis (in seconds)
        retry_on_timeout=True  
    )

except redis.RedisError as e:
    redis_client = None  # Fallback if Redis isn't available
    print(f"⚠️ Redis connection failed: {e}")



qdrant = QdrantClient(url=app.config["QDRANT_URL"],api_key=app.config["QDRANT_API_KEY"])

from app import routes,models