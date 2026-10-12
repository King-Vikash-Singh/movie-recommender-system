
import pickle
import html
import streamlit as st

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# -------------------------------
# Load Saved Model Files
# -------------------------------
@st.cache_resource
def load_model():
    with open("model/movie_list.pkl", "rb") as file:
        movies_data = pickle.load(file)

    with open("model/similarity.pkl", "rb") as file:
        similarity_data = pickle.load(file)

    return movies_data, similarity_data


try:
    movies, similarity = load_model()

except FileNotFoundError:
    st.error(
        "Model files nahi mili. Check karo ki model folder ke andar "
        "movie_list.pkl aur similarity.pkl files maujood hain."
    )
    st.stop()

except Exception as error:
    st.error(f"Model load nahi ho saka: {error}")
    st.stop()


# -------------------------------
# Recommendation Function
# -------------------------------
def recommend(movie):
    matching_movies = movies[movies["title"] == movie]

    if matching_movies.empty:
        return []

    index = matching_movies.index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []

    for i in distances[1:6]:
        movie_name = movies.iloc[i[0]]["title"]
        recommended_movie_names.append(movie_name)

    return recommended_movie_names


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
            word-break: normal;
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

st.write(
    "Select a movie and discover five similar movies!"
)

movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Show Recommendation", type="primary"):

    with st.spinner("Finding recommendations..."):
        recommended_names = recommend(selected_movie)

    if not recommended_names:
        st.warning(
            "Is movie ke liye recommendations nahi mili."
        )

    else:
        st.subheader("Recommended Movies")

        columns = st.columns(len(recommended_names))

        for col, name in zip(columns, recommended_names):
            with col:
                show_movie_card(name)
