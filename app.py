import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4ZmU2ZjJhYTBlNWQ4NjNkN2ZkNGRjNzk5NGNmYmNlOSIsIm5iZiI6MTcyMDk0MzA0MC41MTQyMDgsInN1YiI6IjY2OGY3NzQ2OGUzOWM5YzlmMjEwZWQxOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zYIfFcNM8Y_Z33JOczRQO8PBoU-RlkoFQeFyAiqkLpw"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            full_path = ""  # or a placeholder image URL
        return full_path
    except Exception as e:
        print(f"Error fetching poster: {e}")
        return ""
    
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    # index = 385
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movie_names.pkl','rb'))
movies = pd.DataFrame(movies)
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
print(selected_movie)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]
    for idx in range(5):
        with columns[idx]:
            st.text(recommended_movie_names[idx])
            if recommended_movie_posters[idx]:
                st.image(recommended_movie_posters[idx])
            else:
                st.write("No poster available")