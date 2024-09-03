import streamlit as st
from PIL import Image
import pickle
import requests


# Function for Fetching poster from TMDB API
def fetch_poster(movie_id):
     url = "https://api.themoviedb.org/3/movie/{}?api_key=c028de258d5f25022dedd3d317cdaa34&language=en-US".format(movie_id)
     data=requests.get(url)
     data=data.json()
     poster_path = data['poster_path']
     full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
     return full_path

# Function for fetching movie details from TMDB API
def fetch_movie_details(movie_title):
    url = "https://api.themoviedb.org/3/search/movie?api_key=c028de258d5f25022dedd3d317cdaa34&language=en-US&query={}".format(movie_title)
    data = requests.get(url).json()
    if data['results']:
        movie_data = data['results'][0]
        details = {
            'release_year': movie_data.get('release_date', 'N/A')[:4],
            'genres': [genre['name'] for genre in movie_data.get('genres', [])],  
            'overview': movie_data.get('overview', 'N/A'),
        }
        return details
    else:
        return {}

# Loading movies list from pickle file
movies = pickle.load(open("movies_list.pkl", 'rb'))

# Loading similarity from pickle file 
similarity = pickle.load(open("similarity.pkl", 'rb'))

# Creating list of movies by title
movies_list=movies['title'].values



# Streamlit page design 
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load background image
background_image = Image.open("background2.jpg")

# Display background image
st.image(background_image, use_column_width=True)

# Header
st.title("Movie Recommender System")

# Sidebar selectbox for movie selection
selectvalue = st.sidebar.selectbox("Select a Movie", movies_list)

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[0:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster

# Button to trigger recommendation
if st.sidebar.button("Show Recommendations"):
    movie_name, movie_poster = recommend(selectvalue)
    col1,col2,col3,col4,col5, col6=st.columns(6)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
    with col6:
        st.text(movie_name[5])
        st.image(movie_poster[5])

    # Display recommended movies
    for i in range(len(movie_name)):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(movie_poster[i], width=200)
        with col2:
            st.subheader(movie_name[i])
            movie_details = fetch_movie_details(movie_name[i])
            st.write("Release Year:", movie_details.get('release_year', 'N/A'))
            if movie_details.get('genres'):
                st.write("Genres:", ", ".join(movie_details.get('genres', ['N/A'])))
            else:
                st.write("Genres: N/A")
            st.write("Overview:", movie_details.get('overview', 'N/A'))
        st.write("---")

# Footer
st.markdown(
    """
    <div style="text-align:center; margin-top: 50px;">
        Made with ❤️ by Anuj Kumar Jha
    </div>
    """,
    unsafe_allow_html=True
)
