# Movie Recommendation System

A content-based movie recommendation engine built with Python, Flask, and Streamlit.

## Overview

Recommends movies similar to your favorites using **content-based filtering**. It converts movie descriptions and genres into numerical vectors using **TF-IDF** and finds similar movies using **cosine similarity**.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Recommendation Engine | Python, Scikit-learn (TF-IDF, Cosine Similarity) |
| Data Processing | Pandas, NumPy |
| REST API | Flask |
| Web UI | Streamlit |
| Deployment | Docker, Render |

## Project Structure

```
src/
  data_loader.py      - Load and preprocess movie data
  recommender.py      - TF-IDF + Cosine Similarity engine
  utils.py            - Helper functions
api/
  app.py              - Flask REST API
app.py                - Streamlit web interface
requirements.txt
Dockerfile
render.yaml
Procfile
README.md
```

## Getting Started

### 1. Clone and Install

```bash
git clone https://github.com/ajaykumar7078/Movie-Recommendation-System.git
cd Movie-Recommendation-System
pip install -r requirements.txt
```

### 2. Run the Streamlit App

```bash
streamlit run app.py
```

### 3. Run the Flask API

```bash
python api/app.py
```

### 4. Using Docker

```bash
docker build -t movie-recommender .
docker run -p 5000:5000 movie-recommender
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info and health check |
| GET | `/movies` | List all available movies |
| POST | `/recommend` | Get recommendations |

### Example Request

```bash
curl -X POST http://localhost:5000/recommend \\
  -H "Content-Type: application/json" \\
  -d '{"title": "Inception", "top_n": 5}'
```

## How It Works

1. **Feature Extraction**: Movie overviews and genres are combined into a single text field
2. **TF-IDF Vectorization**: Text is converted into numerical vectors, weighting important words
3. **Cosine Similarity**: Pairwise similarity scores are computed between all movies
4. **Recommendation**: The top-N most similar movies to the user's choice are returned

## Dataset

Built-in sample of 30 popular movies across various genres (Action, Comedy, Drama, Sci-Fi, Animation, Thriller, and more).

---

Built with by **Ajay Chaudhary**
