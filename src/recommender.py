"""Content-based recommendation engine using TF-IDF and cosine similarity."""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedRecommender:
    """Recommends movies based on content similarity using TF-IDF."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        self.tfidf_matrix = None
        self.movie_indices = None
        self.is_fitted = False

    def fit(self, df, feature_column='combined_features'):
        """Fit TF-IDF on movie features and compute similarity matrix."""
        if df.empty:
            raise ValueError("Cannot fit on empty dataframe")
        df = df.copy()
        df[feature_column] = df[feature_column].fillna("")
        self.tfidf_matrix = self.vectorizer.fit_transform(df[feature_column])
        self.movie_indices = pd.Series(df.index, index=df['title'].str.lower()).drop_duplicates()
        self.is_fitted = True

    def recommend(self, df, title, top_n=10):
        """Recommend top_n movies similar to the given title."""
        if not self.is_fitted:
            raise RuntimeError("Recommender not fitted. Call .fit() first.")
        title_lower = title.lower()
        if title_lower not in self.movie_indices.index:
            matches = self.movie_indices[self.movie_indices.index.str.contains(title_lower, na=False)]
            if matches.empty:
                return []
            idx = matches.iloc[0]
        else:
            idx = self.movie_indices[title_lower]

        sim_scores = list(enumerate(self.tfidf_matrix[idx].toarray().flatten()))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n + 1]

        recommendations = []
        for i, score in sim_scores:
            movie = df.iloc[i]
            recommendations.append({
                'title': movie['title'],
                'genres': movie['genres'],
                'overview': movie['overview'],
                'similarity_score': round(float(score), 4)
            })
        return recommendations
