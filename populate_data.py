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
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String,select,text
from sqlalchemy.orm import sessionmaker

# Replace this with your actual PostgreSQL database URL
DATABASE_URL = ''

try:
    # Create database engine
    engine = create_engine(DATABASE_URL)
    print("INFO: Database connection established.")

    # Create a connection
    with engine.connect() as conn:
        print('connected')
        query = text("SELECT * FROM top_movie LIMIT 10")
        result = conn.execute(query)
        print('executed query')
        # Fetch all rows
        rows = result.fetchall()
        print('fetched')
        # Print results
        for row in rows:
            print(row)



#     metadata = MetaData()

#     # Define tables
#     movie = Table(
#         "movie", metadata,
#         Column("id", Integer, primary_key=True),
#         Column("title", String, nullable=False)
#     )

#     top_movie = Table(
#         "top_movie", metadata,
#         Column("id", Integer, primary_key=True),
#         Column("title", String, nullable=False)
#     )

#     # Create tables in PostgreSQL
#     metadata.create_all(engine)
#     print("INFO: Tables created successfully.")

#     # Load CSV files
#     try:
#         movies = pd.read_csv("../movies.csv")
#         # top_movies = pd.read_csv("../top_movies.csv")
#         print(f"INFO: Loaded {len(movies)} movies from CSV.")
#         # print(f"INFO: Loaded {len(top_movies)} top movies from CSV.")
#     except Exception as e:
#         print(f"ERROR: Error loading CSV files - {e}")
#         raise

#     # Insert data into PostgreSQL using session
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     try:
#         with engine.begin() as conn:
#             # for _, row in top_movies.iterrows():
#             #     conn.execute(top_movie.insert().values(id=row['id'], title=row['title']))
#             # print("INFO: Top Movies inserted successfully.")


#             for _, row in movies.iterrows():
#                 conn.execute(movie.insert().values(id=row['id'], title=row['title']))
#                 print(row[id])
#             print("INFO: Movies inserted successfully.")



#     except Exception as e:
#         print(f"ERROR: Error inserting data - {e}")
#         raise

except Exception as e:
    print(f"CRITICAL: Critical error - {e}")

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



