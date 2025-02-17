# Movie Recommendation System 🎥

---
Live Project: [Movie Recommendation System](https://recommend-me.onrender.com)

## 🌟 Description

This is a movie recommender system , which recommends movies based on user's favourite movies. It is based on two datasets available on kaggle. The system live site uses Collaborative Filtering technique and Content based Filtering is also implemented in given jupyter notebooks notebooks. Two diffrent types of datasets are used and combined. I have created vectors from user-movie interaction and populated into Qdrant Vector Database. The core building of similarity model can be seen in Jupyter Notebooks provided in the repository. OMDB Movie API is used to fetch and store meta-data of movies.

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS (Tailwind for styling)
- **Backend**: Flask
- **Database**: SQLite
- **Vector Database**: Qdrant
- **Recommendation Engine**: Collaborative Filtering (with and without Matrix Factorization) and Content Based 
- **Deployment**: Docker, Render (Previously deployed with Docker, later I dropped it)
- **External APIs**: OMDB Movie API (movie meta-data)
- **Server**: Gunicorn

---
## 🛠️ Project Flow

## Demo

## Collaborartive Filtering
- The first dataset contains user-matrix interaction.
- Each user rates some movies - this is interaction. Now a matrix can be imagined with rows being each movie and columns being users and value at particular location is a rating given by user in that column to movie in that row.
- Now, we can consider each row as a Vector Representation of that movie.
- We can apply any type of vector similarity score to get 'closeness' of two movies. Thus we can retrieve 'closest' movies of user's Fav movie.
- image of data

## Content Based Filtering
- The second data consists of meta data of movie for example, plot, cast (lead actor,actress etc.), crew (director,writer etc), rating, year of release, theme.
- I applied diffrent vectorization techniques for descriptive data like plot, nomianal data like cast,crew and theme
- Then combined all of them and result is a vector which fairly represents a movie
- Now applying same similarity score to get closeness we can get our recommendations
- image

## Matrix Factorization
- Matrix factorization is a technique that may help in collaboratibe fitering.
- Not all users rate all movies. Not all movies are seen by users. Thus user-movie rating column a sparse matrix, i.e most of values are 0(zeros)
- Thus recommendations may get poor.
- MF is a technique by which we can predict those missing values and can recommend better movies.
- Following is the matrix factorization applied on the data
- image


