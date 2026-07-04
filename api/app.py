"""Flask API for the Movie Recommendation System."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS
from src.data_loader import load_movies, get_all_titles, get_movie_by_title
from src.recommender import ContentBasedRecommender
from src.utils import format_recommendations_json

app = Flask(__name__)
CORS(app)

df = load_movies()
recommender = ContentBasedRecommender()
recommender.fit(df)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "name": "Movie Recommendation System API",
        "version": "1.0.0",
        "endpoints": {
            "/": "GET - API info",
            "/movies": "GET - List all movies",
            "/recommend": "POST - Get recommendations"
        },
        "total_movies": len(df)
    })

@app.route("/movies", methods=["GET"])
def list_movies():
    return jsonify({"count": len(df), "movies": get_all_titles(df)})

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Please provide a 'title' in the request body"}), 400
    title = data["title"]
    top_n = data.get("top_n", 10)
    movie = get_movie_by_title(df, title)
    if movie is None:
        return jsonify({
            "error": f"Movie '{title}' not found.",
            "available_movies": get_all_titles(df)
        }), 404
    recommendations = recommender.recommend(df, movie["title"], top_n=top_n)
    return jsonify({
        "input_title": movie["title"],
        "input_genres": movie["genres"],
        "count": len(recommendations),
        "recommendations": format_recommendations_json(recommendations)
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
