from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from qdrant_client import QdrantClient

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
cache = Cache(app)
qdrant = QdrantClient(url=app.config["QDRANT_URL"],api_key=app.config["QDRANT_API_KEY"])

from app import routes,models