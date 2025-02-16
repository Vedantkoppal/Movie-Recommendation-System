from app import app
from flask import render_template,jsonify,request
from app.models import Movie,TopMovie
from app.recommend import recommedfinal
from app import cache
import requests


@cache.memoize(86400)  # Cache for 1 day
def movie_api(title):
    print(f"Fetching from API: {title}")
    
    params = {"apikey": app.config["OMDB_API_KEY"], "t": title}
    try:
        response = requests.get(app.config["OMDB_URL"], params=params)
        response.raise_for_status()  # Raise an error for 4xx/5xx responses
        data = response.json()
    except:
        data = {"Title": title, "Plot": "Not Available", "Poster": ""}  # Default response
    
    return data  # Only return a serializable dict (not a Response object)


# @app.route('/')
# def home():
#     movie_titles = TopMovie.query.paginate(page = 1,per_page = 10).with_entities(TopMovie.title).limit(5).all()
#     movie_metadata = [movie_api(title) for title in movie_titles]
#     return render_template('home.html',movies = movie_metadata)

@app.route('/')
@app.route('/page/<int:page>')
def home(page=1):
    per_page = 16  # Number of movies per page
    paginated_movies = TopMovie.query.paginate(page=page, per_page=per_page)

    # Fetch metadata for current page's movies
    movie_metadata = [movie_api(movie.title) for movie in paginated_movies.items]

    return render_template(
        'home.html', 
        movies=movie_metadata,
        pagination=paginated_movies
    )


@app.route('/index')
def index():
    return "Hello Not world"


@app.route('/recommend')
def search():
    return render_template('recommend.html') 

# @app.route('/search', methods=['GET'])
# def search_movies():
#     query = request.args.get('q', '')
#     if query:
#         start_matches = Movie.query.filter(Movie.title.ilike(f"{query}%")).limit(10).all()
#         return jsonify([{'id': movie.id, 'name': movie.title} for movie in movies])
#     return jsonify([])

@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])

    # Movies that start with the query first
    start_matches = Movie.query.filter(Movie.title.ilike(f"{query}%")).limit(10).all()
    remaining_limit = 10 - len(start_matches)

    # If we still need more results, fetch similar matches (excluding already fetched)
    similar_matches = []
    if remaining_limit > 0:
        similar_matches = (
            Movie.query.filter(Movie.title.ilike(f"%{query}%"))
            .filter(~Movie.id.in_([m.id for m in start_matches]))  # Exclude already fetched movies
            .limit(remaining_limit)
            .all()
        )

    # Combine results (movies that start with query appear first)
    movies = start_matches + similar_matches
    print(movies[0].title)
    return jsonify([{'id': movie.id, 'title': movie.title} for movie in movies]) 

@app.route('/get-similar-movies', methods=['POST'])
def get_similar_movies():
    data = request.get_json()
    
    movie_ids = data.get('movie_ids', [])
    # print("selected ids :",movie_ids) 
    # Get similar movies based on the selected movie IDs
    similar_movie_ids = recommedfinal(movie_ids)
    # print("type of ids :",type(similar_movie_ids))

    # print("suggested :",similar_movie_ids)
    similar_movies = Movie.query.filter(Movie.id.in_(similar_movie_ids)).all()
    # print(similar_movies)
    similar_movies_data = [
        {"id": movie.id, "title": movie.title} 
        for movie in similar_movies
    ]
    # print(similar_movies_data)
    # Return the similar movies to the frontend
    return jsonify(similar_movies_data)
