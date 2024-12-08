import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list=(sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1]))[1:16]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters


movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name=st.selectbox(
    'Select a movie for recommendations:',
    movies['title'].values
)

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'show_more' not in st.session_state:
    st.session_state.show_more = False
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

# Recommend button logic

if st.button('Recommend'):
    st.session_state.show_more = True
    st.session_state.button_clicked = False
    st.session_state.recommendations = recommend(selected_movie_name)

# Display recommendations if available
if st.session_state.recommendations:
    rows = [st.container() for _ in range(3)]
    cols_per_row = [r.columns(5) for r in rows]
    cols = [column for row in cols_per_row for column in row]
    names, posters = st.session_state.recommendations
    for image_index, movie_image in enumerate(posters):
        if image_index==5:
            break
        cols[image_index].image(posters[image_index])
    for text_index, movie_text in enumerate(names):
        if text_index==5:
            break
        cols[text_index].text(names[text_index])
    if st.session_state.show_more:
        if st.button('Show More',disabled=st.session_state.button_clicked):

            for image_index, movie_image in enumerate(posters,start=5):
                if image_index == 15:
                    break
                cols[image_index].image(posters[image_index])
            for text_index, movie_text in enumerate(names,start=5):
                if text_index == 15:
                    break
                cols[text_index].text(names[text_index])

            st.session_state.button_clicked = True
