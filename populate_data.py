# from app import app,db
# from app.models import Movie, TopMovie
# import pandas as pd

# movies = pd.read_csv('../movies.csv')
# top_movies = pd.read_csv('../top_movies.csv')


# with app.app_context():
#     for _, row in movies.iterrows():
#         movie = Movie(id=row['id'],title=row['title'])
#         db.session.add(movie)
#     db.session.commit()
# print('1 done')
# with app.app_context():
#     for _, row in top_movies.iterrows():
#         movie = TopMovie(id=row['id'],title=row['title'])
#         db.session.add(movie)
#     db.session.commit()

# print('2 done')


import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker

# Replace this with your actual PostgreSQL database URL
DATABASE_URL = 

# Create database engine
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define tables
movie_table = Table(
    "movie", metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False)
)

top_movie_table = Table(
    "top_movie", metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False)
)

# Create tables in PostgreSQL
metadata.create_all(engine)

# Load CSV files
movies = pd.read_csv("../movies.csv")
top_movies = pd.read_csv("../top_movies.csv")

# Insert data into PostgreSQL using session
Session = sessionmaker(bind=engine)
session = Session()

with engine.begin() as conn:
    for _, row in movies.iterrows():
        conn.execute(movie_table.insert().values(id=row['id'], title=row['title']))
    print("Movies inserted.")

    for _, row in top_movies.iterrows():
        conn.execute(top_movie_table.insert().values(id=row['id'], title=row['title']))
    print("Top Movies inserted.")


# import pandas as pd
# from sqlalchemy import create_engine, MetaData, Table
# from sqlalchemy.orm import sessionmaker

# # Replace this with your actual PostgreSQL database URL
# DATABASE_URL = 
# # Create database engine
# engine = create_engine(DATABASE_URL)
# metadata = MetaData(bind=engine)
# Session = sessionmaker(bind=engine)
# session = Session()

# # Load CSV files
# movies = pd.read_csv("../movies.csv")
# top_movies = pd.read_csv("../top_movies.csv")

# # Get the tables
# movie_table = Table("movie", metadata, autoload_with=engine)
# top_movie_table = Table("top_movie", metadata, autoload_with=engine)

# # Insert data into movie table
# with engine.connect() as conn:
#     for _, row in movies.iterrows():
#         conn.execute(movie_table.insert().values(id=row['id'], title=row['title']))
#     conn.commit()

# print("Movies inserted.")

# # Insert data into top_movie table
# with engine.connect() as conn:
#     for _, row in top_movies.iterrows():
#         conn.execute(top_movie_table.insert().values(id=row['id'], title=row['title']))
#     conn.commit()

# print("Top Movies inserted.")



