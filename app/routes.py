from flask import render_template,jsonify,request
from app import app
from app.models import Movie,MovieMain
from app.recommend import recommedfinal

def data():
    lm = ['Interstellar','Shaswshank','Toy Story','Fight Club']
    return lm

@app.route('/')
def home():
    # movies = data()
    movies = Movie.query.limit(30).all()
    return render_template('home.html',movies = movies)

@app.route('/index')
def index():
    return "Hello World"


@app.route('/recommend')
def search():
    return render_template('recommend.html') 

@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('q', '')
    if query:
        movies = MovieMain.query.filter(MovieMain.title.ilike(f"%{query}%")).limit(5).all()
        return jsonify([{'id': movie.id, 'name': movie.title} for movie in movies])
    return jsonify([])

@app.route('/get-similar-movies', methods=['POST'])
def get_similar_movies():
    data = request.get_json()
    
    movie_ids = data.get('movie_ids', [])
    # print("selected ids :",movie_ids) 
    # Get similar movies based on the selected movie IDs
    similar_movie_ids = recommedfinal(movie_ids)
    # print("type of ids :",type(similar_movie_ids))

    # print("suggested :",similar_movie_ids)
    similar_movies = MovieMain.query.filter(MovieMain.id.in_(similar_movie_ids)).all()
    # print(similar_movies)
    similar_movies_data = [
        {"id": movie.id, "title": movie.title} 
        for movie in similar_movies
    ]
    # print(similar_movies_data)
    # Return the similar movies to the frontend
    return jsonify(similar_movies_data)
