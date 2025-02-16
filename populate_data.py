from app import app,db
from app.models import Movie, TopMovie
import pandas as pd

movies = pd.read_csv('../movies.csv')
top_movies = pd.read_csv('../top_movies.csv')


with app.app_context():
    for _, row in movies.iterrows():
        movie = Movie(id=row['id'],title=row['title'])
        db.session.add(movie)
    db.session.commit()
print('1 done')
with app.app_context():
    for _, row in top_movies.iterrows():
        movie = TopMovie(id=row['id'],title=row['title'])
        db.session.add(movie)
    db.session.commit()

print('2 done')
