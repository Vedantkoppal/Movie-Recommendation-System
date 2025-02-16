# from app import app 
# from app.models import TopMovie

# with app.app_context():
#     movie_titles = TopMovie.query.with_entities(TopMovie.title).all()
#     print([title[0] for title in movie_titles])

# from app.routes import movie_api

# jls_extract_var = 'interstellar'
# print(movie_api(jls_extract_var))

from app import cache

print(cache.cache._cache.keys())