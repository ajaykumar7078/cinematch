"""Flask REST API for the Movie Recommendation System."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.data_loader import load_movies, get_movie_by_title, get_all_titles, get_all_genre_names
from src.recommender import ContentBasedRecommender
from src.genre_explorer import GenreExplorer
from src.utils import format_recommendations_json

app = Flask(__name__)
CORS(app)

print("Loading TMDB 5000 dataset...")
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'tmdb_5000_movies.csv.gz')
df = load_movies(DATA_PATH)
print(f"Loaded {len(df)} movies.")

print("Fitting content-based recommender...")
recommender = ContentBasedRecommender(max_features=8000)
recommender.fit(df)
print("Recommender ready!")

explorer = GenreExplorer(df)
ALL_GENRES = get_all_genre_names(df)
print(f"Available genres ({len(ALL_GENRES)}): {', '.join(ALL_GENRES)}")

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "name": "Movie Recommendation System API",
        "version": "2.0.0",
        "total_movies": len(df),
        "available_genres": ALL_GENRES,
        "endpoints": {
            "/": "GET - API info","/movies": "GET - Search/list movies","/movies/<title>": "GET - Movie details","/genres": "GET - List all genres","/genres/<genre>/top": "GET - Top rated in genre","/genres/<genre>/popular": "GET - Most popular in genre","/genres/<genre>/latest": "GET - Latest releases","/genres/<genre>/gems": "GET - Underrated gems","/genres/<genre>/stats": "GET - Genre statistics","/multi-genre": "POST - Multi-genre search","/recommend": "POST - Similar movies"
        }
    })

@app.route("/movies", methods=["GET"])
def list_movies():
    q = request.args.get("q", "").strip().lower()
    page = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 50)), 200)
    if q: filtered = df[df['title'].str.lower().str.contains(q, na=False)]
    else: filtered = df
    total = len(filtered)
    start = (page - 1) * per_page
    end = start + per_page
    movies_data = []
    for _, row in filtered.iloc[start:end].iterrows():
        movies_data.append({"title": row["title"], "genres": row["genres_str"], "vote_average": float(row["vote_average"]), "vote_count": int(row["vote_count"]), "release_year": int(row["release_year"]), "popularity": float(row["popularity"])})
    return jsonify({"total": total, "page": page, "per_page": per_page, "total_pages": (total+per_page-1)//per_page, "movies": movies_data})

@app.route("/movies/<path:title>", methods=["GET"])
def movie_detail(title):
    movie = get_movie_by_title(df, title)
    if movie is None: return jsonify({"error": f"Movie '{title}' not found"}), 404
    return jsonify({"title": movie["title"], "genres": movie["genres_str"], "overview": movie["overview"], "vote_average": float(movie["vote_average"]), "vote_count": int(movie["vote_count"]), "popularity": float(movie["popularity"]), "release_date": movie["release_date"], "release_year": int(movie["release_year"])})

@app.route("/genres", methods=["GET"])
def list_genres():
    genre_data = []
    for genre in ALL_GENRES:
        mask = df['genres_str'].str.contains(genre, case=False, na=False)
        genre_data.append({"name": genre, "movie_count": int(mask.sum()), "avg_rating": round(df[mask]['vote_average'].mean(), 2)})
    return jsonify({"genres": sorted(genre_data, key=lambda x: -x['movie_count'])})

@app.route("/genres/<genre>/top", methods=["GET"])
def genre_top(genre):
    return jsonify({"genre": genre, "mode": "top_rated", "movies": explorer.top_by_genre(genre, top_n=int(request.args.get("top_n",20)))})

@app.route("/genres/<genre>/popular", methods=["GET"])
def genre_popular(genre):
    return jsonify({"genre": genre, "mode": "popular", "movies": explorer.popular_by_genre(genre, top_n=int(request.args.get("top_n",20)))})

@app.route("/genres/<genre>/latest", methods=["GET"])
def genre_latest(genre):
    return jsonify({"genre": genre, "mode": "latest", "movies": explorer.latest_by_genre(genre, top_n=int(request.args.get("top_n",20)))})

@app.route("/genres/<genre>/gems", methods=["GET"])
def genre_gems(genre):
    return jsonify({"genre": genre, "mode": "gems", "movies": explorer.underrated_gems(genre, top_n=int(request.args.get("top_n",15)))})

@app.route("/genres/<genre>/stats", methods=["GET"])
def genre_stats(genre):
    return jsonify({"genre": genre, "stats": explorer.genre_stats(genre)})

@app.route("/multi-genre", methods=["POST"])
def multi_genre():
    data = request.get_json()
    if not data or "genres" not in data: return jsonify({"error": "Provide genres list"}), 400
    return jsonify({"genres": data["genres"], "movies": explorer.multi_genre_search(data["genres"], sort_by=data.get("sort_by","vote_average"), top_n=int(data.get("top_n",20)))})

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    if not data or "title" not in data: return jsonify({"error": "Provide title"}), 400
    movie = get_movie_by_title(df, data["title"])
    if movie is None: return jsonify({"error": f"Movie '{data['title']}' not found"}), 404
    recs = recommender.recommend(df, movie["title"], top_n=int(data.get("top_n",10)))
    return jsonify({"input_title": movie["title"], "input_genres": movie["genres_str"], "input_year": int(movie["release_year"]), "input_rating": float(movie["vote_average"]), "count": len(recs), "recommendations": format_recommendations_json(recs)})

@app.errorhandler(404)
def not_found(e): return jsonify({"error": "Not found"}), 404
@app.errorhandler(500)
def server_error(e): return jsonify({"error": "Server error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
