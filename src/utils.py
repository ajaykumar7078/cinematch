"""Utility functions for formatting and display."""

def format_recommendations_json(recommendations):
    return [
        {
            "title": rec["title"],
            "genres": rec.get("genres", ""),
            "overview": rec.get("overview", ""),
            "vote_average": rec.get("vote_average", 0),
            "vote_count": rec.get("vote_count", 0),
            "popularity": rec.get("popularity", 0),
            "release_year": rec.get("release_year", 0),
            "similarity_score": rec.get("similarity_score", 0)
        }
        for rec in recommendations
    ]
