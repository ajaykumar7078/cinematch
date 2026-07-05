# 🎬 Movie Recommendation System Pro

A powerful, multi-mode movie recommendation engine built with **Python, Flask, Streamlit**, and the **TMDB 5000 dataset** (4,803 movies).

## Features
- **🎯 Similar Movie Finder** — TF-IDF + cosine similarity on overviews, genres & keywords
- **🔍 Genre Explorer** — Browse top-rated, most popular, or latest releases by genre
- **🎭 Multi-Genre Search** — Find movies matching multiple genres (e.g., Horror + Thriller)
- **💎 Hidden Gems** — Discover underrated high-rated movies with fewer votes
- **📊 Genre Stats** — Compare genres by movie count, avg rating, top picks

## Dataset
**4,803 movies** from TMDB across **20 genres**: Drama (2,297), Comedy (1,722), Thriller (1,274), Action (1,154), Romance (894), Adventure (790), Crime (696), Sci-Fi (535), Horror (519), Family (513), Fantasy (424), Mystery (348), Animation (234), History (197), Music (185), War (144), Documentary (110), Western (82), Foreign (34), TV Movie (8)

## Project Structure
```
├── src/
│   ├── data_loader.py       # Load & parse TMDB dataset (JSON genres/keywords)
│   ├── recommender.py       # TF-IDF + cosine similarity engine
│   ├── genre_explorer.py    # Genre-based filtering & discovery (5 modes)
│   └── utils.py             # Formatting helpers
├── api/
│   └── app.py               # Flask REST API (12+ endpoints)
├── data/
│   └── tmdb_5000_movies.csv.gz # 4,803 movies (gzipped)
├── app.py                   # Streamlit web interface (5 modes)
├── requirements.txt
├── Dockerfile
├── render.yaml
└── README.md
```

## Quick Start
```bash
git clone https://github.com/ajaykumar7078/Movie-Recommendation-System.git
cd Movie-Recommendation-System
pip install -r requirements.txt
streamlit run app.py   # Web UI at localhost:8501
python api/app.py      # Flask API at localhost:5000
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info & available genres |
| GET | `/movies?q=&page=&per_page=` | Search/browse movies |
| GET | `/movies/<title>` | Movie details |
| GET | `/genres` | All genres with counts |
| GET | `/genres/<genre>/top` | Top rated in genre |
| GET | `/genres/<genre>/popular` | Most popular |
| GET | `/genres/<genre>/latest` | Latest releases |
| GET | `/genres/<genre>/gems` | Underrated gems |
| GET | `/genres/<genre>/stats` | Genre statistics |
| POST | `/multi-genre` | Multi-genre search |
| POST | `/recommend` | Similar movies |

### Example
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"title": "Inception", "top_n": 5}'
```

## Tech Stack
Python, Scikit-learn (TF-IDF), Pandas, Flask, Streamlit, Docker

---
Built with ❤️ by **Ajay Chaudhary**
