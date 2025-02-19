# from app import app 
# from app.models import TopMovie

# with app.app_context():
#     movie_titles = TopMovie.query.with_entities(TopMovie.title).all()
#     print([title[0] for title in movie_titles])

# from app.routes import movie_api

# jls_extract_var = 'interstellar'
# print(movie_api(jls_extract_var))
# from app import app
# import requests
# from app import cache/
# from app.routes import movie_api
# cache.clear()
# @cache.memoize(86400)  # Cache for 1 day
# def movie_api(title):
#     print(f"Fetching from API: {title}")
    
#     params = {"apikey": app.config["OMDB_API_KEY"], "t": title}
#     try:
#         response = requests.get(app.config["OMDB_URL"], params=params)
#         response.raise_for_status()  # Raise an error for 4xx/5xx responses
#         data = response.json()
#     except Exception as e:
#         print(e)

#     if(data['Response'] == 'False'):
#         data = {"Title": title, "Plot": "Poster Not Found", "Poster": ""}

#     return data  # Only return a serializable dict (not a Response object)
# `
# print(movie_api('/千と千尋の神隠し'))

# from app import qdrant

# print(qdrant.get_collections())

# from app.recommend import recommend_qdrant

# recommend_qdrant([1])

# from app import redis_client
# page_cache_key = f"page_html_3"  # Replace with actual key
# redis_client.delete(page_cache_key)
# print(f"✅ Cache cleared for: {page_cache_key}")
