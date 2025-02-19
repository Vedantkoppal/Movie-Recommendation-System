from flask import render_template,jsonify,request,session
import requests
import json

from app import app,redis_client
from app.models import Movie,TopMovie
from app.recommend import recommend_qdrant




@app.route('/index')
def index():
    return "Hello Not world"

# @app.route('/')
# @app.route('/page/<int:page>')
# @cache.cached(timeout=300, key_prefix=lambda: f"page_{request.view_args.get('page',1)}")
# def home(page=1):
#     print(f'This is home page : {page}')
#     per_page = 16  # Number of movies per page
#     paginated_movies = TopMovie.query.paginate(page=page, per_page=per_page)

#     # Fetch metadata for current page's movies
#     movie_metadata = [movie_api(movie.title) for movie in paginated_movies.items]
#     print('home page not from cache')
#     return render_template(
#         'home.html', 
#         movies=movie_metadata,
#         pagination=paginated_movies
#     )

@app.route('/')
@app.route('/page/<int:page>')
def home(page=1):
    print(f'This is home page : {page}')
    
    cache_key = f"page_html_{page}"
    
    # Check Redis cache for full HTML
    try:
        cached_html = redis_client.get(cache_key)
        if cached_html:
            print("✅ Home Page HTML from Redis Cache")
            return cached_html  # Directly return cached HTML
    except Exception as e:
        print(f"⚠️ Redis Error: {e}")

    # If not cached, fetch from DB
    per_page = 16  
    paginated_movies = TopMovie.query.paginate(page=page, per_page=per_page)

    # Fetch metadata for current page's movies
    movie_metadata = [movie_api(movie.title) for movie in paginated_movies.items]
    print('🌐 Home page not from cache')

    # Render the HTML
    rendered_html = render_template(
        'home.html', 
        movies=movie_metadata,
        pagination=paginated_movies
    )

    # Store rendered HTML in Redis (cache for 5 minutes)
    try:
        redis_client.setex(cache_key, 300, rendered_html)
    except Exception as e:
        print(f"⚠️ Redis Caching Error: {e}")

    return rendered_html  # Return rendered HTML page



@app.route('/recommend')
def search():
    return render_template('recommend.html') 


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
    return jsonify([{'id': movie.id, 'title': movie.title} for movie in movies]) 


# OMDB Route
@app.route("/api/movie") 
def get_movie():
    title = request.args.get("title")
    if not title:
        return jsonify({"error": "Title is required"}), 400
    
    movie_data = movie_api(title)  # Calls `movie_api()`
    return jsonify(movie_data)  # Sends JSON response



def movie_api(title):

    # Handle Redis connection issues
    if redis_client:
        try:
            cached_data = redis_client.get(title)
            if cached_data:
                print("✅ From Redis Cache")
                return json.loads(cached_data)
        except redis.RedisError as e:
            print(f"⚠️ Redis Error: {e}")
    

    # Query OMDB API
    params = {"apikey": app.config.get("OMDB_API_KEY"), "t": title}
    try:
        response = requests.get(app.config.get("OMDB_URL"), params=params, timeout=5)  # Timeout after 5 sec
        response.raise_for_status()  # Raise error for 4xx/5xx HTTP responses
        data = response.json()
        print("🌐 From OMDB API")

    except requests.exceptions.Timeout:
        print("⚠️ OMDB API Timeout")
        return {"error": "OMDB API timeout, please try again later."}

    except requests.exceptions.ConnectionError:
        print("⚠️ OMDB API Connection Error")
        return {"error": "Unable to connect to OMDB API, please check your internet connection."}

    except requests.exceptions.HTTPError as http_err:
        print(f"⚠️ HTTP Error: {http_err}")
        return {"error": f"OMDB API returned an error: {http_err}"}

    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")
        return {"error": "An unexpected error occurred while fetching movie data."}

    # Handle OMDB API movie not found case
    if data.get('Response') == 'False':
        print("❌ Movie Not Found in OMDB")
        data = {"Title": title, "Plot": "Movie not found", "Poster": ""}

    # Store result in Redis (if available)
    if redis_client:
        try:
            redis_client.setex(title, 86400, json.dumps(data))  # Cache for 1 day
        except redis.RedisError as e:
            print(f"⚠️ Failed to cache in Redis: {e}")

    return data 


@app.route('/get-similar-movies', methods=['POST'])
def get_similar_movies():
    data = request.get_json()
    
    movie_ids = data.get('movie_ids', [])

    # Get similar movies based on the selected movie IDs
    similar_movie_ids = recommend_qdrant(movie_ids)

    similar_movies = Movie.query.filter(Movie.id.in_(similar_movie_ids)).all()
    # print(similar_movies)
    similar_movies_data = [
        {"id": movie.id, "title": movie.title} 
        for movie in similar_movies
    ]

    return jsonify(similar_movies_data)


@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

# unique visitors
@app.before_request
def track_visits():
    """Tracks total visitors, unique visitors, and active visitors"""
    today = datetime.date.today().strftime("%Y-%m-%d")  # Today's date

    # Increment total visitors (every request counts)
    redis_client.incr("total_visitors")

    # Track unique visitors using Flask session
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())  # Assign a unique session ID
        redis_client.sadd("unique_visitors", session["user_id"])  # Add user to unique visitors
        redis_client.sadd(f"unique_visitors:{today}", session["user_id"])  # Unique visitors today

    # Increment daily visitor count
    redis_client.incr(f"daily_visitors:{today}")

    # Track active visitors (users active in the last 5 minutes)
    redis_client.sadd("active_users", session["user_id"])
    redis_client.expire("active_users", 300)  # Auto-remove inactive users after 5 min


@app.route('/stats')
def get_stats():
    """Returns site analytics"""
    today = datetime.date.today().strftime("%Y-%m-%d")

    stats = {
        "total_visitors": int(redis_client.get("total_visitors") or 0),
        "total_unique_visitors": redis_client.scard("unique_visitors"),
        "daily_visitors": int(redis_client.get(f"daily_visitors:{today}") or 0),
        "daily_unique_visitors": redis_client.scard(f"unique_visitors:{today}"),
        "current_active_visitors": redis_client.scard("active_users")
    }
    return jsonify(stats)


@app.route('/dashboard')
def home():
    """Main page"""
    return '''
    <h2>Welcome to the Site</h2>
    <p><a href="/stats">View Site Analytics</a></p>
    '''

