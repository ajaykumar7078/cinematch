"""Content-based recommendation engine using TF-IDF and cosine similarity."""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender:
    def __init__(self, max_features=8000):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=max_features, max_df=0.85, min_df=2, ngram_range=(1,2))
        self.tfidf_matrix = None
        self.movie_indices = None
        self.is_fitted = False

    def fit(self, df, feature_column='combined_features'):
        if df.empty:
            raise ValueError("Cannot fit on empty dataframe")
        df = df.copy()
        df[feature_column] = df[feature_column].fillna("")
        self.tfidf_matrix = self.vectorizer.fit_transform(df[feature_column])
        self.movie_indices = pd.Series(df.index, index=df['title'].str.lower()).drop_duplicates()
        self.is_fitted = True

    def recommend(self, df, title, top_n=10, exclude_title=None):
        if not self.is_fitted:
            raise RuntimeError("Recommender not fitted yet. Call .fit() first.")
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
        results = []
        seen_titles = set()
        if exclude_title:
            seen_titles.add(exclude_title.lower())
        for i, score in sim_scores[1:]:
            movie = df.iloc[i]
            title_key = movie['title'].lower()
            if title_key in seen_titles:
                continue
            seen_titles.add(title_key)
            results.append({
                'title': movie['title'],
                'genres': movie['genres_str'],
                'overview': movie['overview'][:300] if pd.notna(movie['overview']) else '',
                'vote_average': float(movie['vote_average']),
                'vote_count': int(movie['vote_count']),
                'popularity': float(movie['popularity']),
                'release_year': int(movie['release_year']),
                'similarity_score': round(float(score), 4)
            })
            if len(results) >= top_n:
                break
        return results
