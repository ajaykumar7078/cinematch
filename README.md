# 🎬 Movie Recommendation System Pro

Multi-mode recommendation engine with **4,803 movies** from TMDB.

## Features
- **🎯 Similar Movie Finder** — TF-IDF + cosine similarity recommendations
- **🔍 Genre Explorer** — Browse top/popular/latest by genre
- **🎭 Multi-Genre** — Movies matching multiple genres
- **💎 Hidden Gems** — Underrated high-rated movies
- **📊 Genre Stats** — Compare genres

## Quick Start
```bash
git clone https://github.com/ajaykumar7078/Movie-Recommendation-System.git
cd Movie-Recommendation-System
pip install -r requirements.txt
streamlit run app.py  # Web UI at :8501
python api/app.py     # API at :5000
```

## API
POST `/recommend` `{"title": "Inception", "top_n": 5}`
GET `/genres/<genre>/top`
GET `/genres/<genre>/popular`
POST `/multi-genre` `{"genres": ["Horror","Thriller"]}`
GET `/genres/<genre>/gems`
GET `/genres/<genre>/stats`

## Tech
Python, Scikit-learn, Flask, Streamlit, Docker

Built by **Ajay Chaudhary**
