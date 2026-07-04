"""Utility functions for the Movie Recommendation System."""

def format_recommendations(recommendations):
    """Format recommendations into a readable string."""
    if not recommendations:
        return "No recommendations found. Try a different movie title."
    lines = ["\U0001f3ac **Top Recommended Movies:**\n"]
    for i, rec in enumerate(recommendations, 1):
        score_pct = rec['similarity_score'] * 100
        lines.append(f"{i}. **{rec['title']}** - {score_pct:.1f}% match\n   \U0001f3f7\ufe0f {rec['genres']}\n")
    return "\n".join(lines)

def format_recommendations_json(recommendations):
    """Format recommendations as a clean JSON-compatible list."""
    return [
        {"title": rec["title"], "genres": rec["genres"],
         "overview": rec["overview"], "similarity_score": rec["similarity_score"]}
        for rec in recommendations
    ]
