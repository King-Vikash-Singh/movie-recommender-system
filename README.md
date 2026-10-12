# 🎬 Movie Recommender System

A Machine Learning web application that recommends five similar movies based on the movie selected by the user.

## Features
- Select a movie from a dropdown menu.
- Get five similar movie recommendations.
- Interactive web interface built with Streamlit.
- Content-based movie recommendation system.
- Movie titles displayed in stylish cards.

## Technologies Used
- Python
- Pandas
- NumPy
- Streamlit
- Machine Learning

## Project Structure
- `app.py` — Main Streamlit application.
- `model/movie_list.pkl` — Saved movie data.
- `model/similarity.pkl` — Precomputed similarity matrix.
- `Movie_Recommender_system.ipynb` — Model development notebook.
- `tmdb_5000_movies.csv` — Movie dataset.
- `tmdb_5000_credits.csv` — Movie credits dataset.
- `requirements.txt` — Project dependencies.

## Installation and Usage

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

## Dataset
This project uses the TMDB 5000 Movies and Credits datasets.

## Author
Vikash Singh