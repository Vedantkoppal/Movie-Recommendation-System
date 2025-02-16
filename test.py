from app import app 
from app.models import TopMovie

with app.app_context():
    movie_titles = TopMovie.query.with_entities(TopMovie.title).all()
    print([title[0] for title in movie_titles])