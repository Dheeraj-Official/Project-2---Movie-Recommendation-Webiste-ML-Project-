import streamlit as st
import pickle
import requests

# Load data
data = pickle.load(open('model/movies.pkl', 'rb'))
similarity = pickle.load(open("model/similarity.pkl", 'rb'))

# Base URL for poster images
base_poster_path = "https://image.tmdb.org/t/p/original"

# Function to fetch movie poster by movie ID
def fetch_poster(movie_id):
    api_key = '3012e518de979ff28900bb73958bd314'
    search_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(search_url)
    data = response.json()
    return base_poster_path + data["poster_path"]

# Function to recommend movies
def recommend(movie_name):
    movie_index = data[data["title"] == movie_name].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        recommended_movies.append(data["title"][i[0]])
        id = data["id"][i[0]]
        poster = fetch_poster(id)
        recommended_posters.append(poster)
    
    return recommended_movies, recommended_posters

# Streamlit application
st.set_page_config(page_title="Movie Recommendation", page_icon="🎬")

# Title and description
st.title("🎥 Movie Recommendation 🍿")
st.markdown(
    "Welcome to our movie recommendation app! Select a movie from the dropdown "
    "and click **Recommend** to find similar movies."
)

# Movie selection dropdown
selected_movie = st.selectbox("Select a movie", data["title"].values)

# Recommendation button
if st.button("Recommend"):
    recommended_movies, posters = recommend(selected_movie)
    
    # Display recommended movies and posters
    st.subheader("Recommended Movies")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    for col, movie, poster in zip([col1, col2, col3, col4, col5], recommended_movies, posters):
        with col:
            st.text(movie)
            st.image(poster, use_column_width=True)
