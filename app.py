import pickle
import html
from pathlib import Path

import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
MOVIE_FILE = BASE_DIR / "model" / "movie_list.pkl"


# -------------------------------
# Load Movie Data
# -------------------------------
@st.cache_resource
def load_model():
    with open(MOVIE_FILE, "rb") as file:
        movies_data = pickle.load(file)

    if "title" not in movies_data.columns:
        raise ValueError("Movie data mein 'title' column nahi mila.")

    if "tags" not in movies_data.columns:
        raise ValueError(
            "Movie data mein 'tags' column nahi mila. "
            "Notebook se movie_list.pkl check karo."
        )

    movies_data = movies_data.reset_index(drop=True).copy()
    movies_data["tags"] = movies_data["tags"].fillna("").astype(str)

    vectorizer = CountVectorizer(max_features=5000)
    vectors = vectorizer.fit_transform(movies_data["tags"])

    return movies_data, vectors


try:
    movies, vectors = load_model()

except Exception as error:
    st.error(f"Model load nahi ho saka: {error}")
    st.stop()


# -------------------------------
# Recommendation Function
# -------------------------------
def recommend(movie):
    matching_movies = movies.index[movies["title"] == movie].tolist()

    if not matching_movies:
        return []

    index = matching_movies[0]

    # Calculate similarity for the selected movie only.
    scores = cosine_similarity(vectors[index], vectors).flatten()

    # Highest similarity first; exclude the selected movie.
    ranked_indices = scores.argsort()[::-1]
    recommended_names = []

    for movie_index in ranked_indices:
        if movie_index == index:
            continue

        name = movies.iloc[movie_index]["title"]

        if name not in recommended_names:
            recommended_names.append(name)

        if len(recommended_names) == 5:
            break

    return recommended_names


# -------------------------------
# Movie Name Card
# -------------------------------
def show_movie_card(movie_name):
    safe_name = html.escape(str(movie_name))

    st.markdown(
        f"""
        <div style="
            height: 280px;
            width: 100%;
            box-sizing: border-box;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 18px;
            background: linear-gradient(145deg, #20242c, #343b49);
            border: 1px solid #555e6d;
            border-radius: 12px;
            color: white;
            font-size: 20px;
            font-weight: bold;
            overflow-wrap: anywhere;
        ">
            {safe_name}
        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------------------
# Streamlit User Interface
# -------------------------------
st.title("🎬 Movie Recommender System")
st.write("Select a movie and discover five similar movies!")

movie_list = movies["title"].dropna().tolist()

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Show Recommendation", type="primary"):
    with st.spinner("Finding recommendations..."):
        recommended_names = recommend(selected_movie)

    if not recommended_names:
        st.warning("Is movie ke liye recommendations nahi mili.")
    else:
        st.subheader("Recommended Movies")

        columns = st.columns(len(recommended_names))

        for col, name in zip(columns, recommended_names):
            with col:
                show_movie_card(name)