"""Genre Explorer — multi-mode movie discovery based on genre."""
import pandas as pd

class GenreExplorer:
    def __init__(self, df):
        self.df = df

    def top_by_genre(self, genre, min_votes=100, top_n=20):
        mask = self.df['genres_str'].str.contains(genre, case=False, na=False)
        filtered = self.df[mask].copy()
        filtered = filtered[filtered['vote_count'] >= min_votes]
        filtered = filtered.sort_values('vote_average', ascending=False)
        return self._format_movies(filtered.head(top_n))

    def popular_by_genre(self, genre, min_votes=50, top_n=20):
        mask = self.df['genres_str'].str.contains(genre, case=False, na=False)
        filtered = self.df[mask].copy()
        filtered = filtered[filtered['vote_count'] >= min_votes]
        filtered = filtered.sort_values('popularity', ascending=False)
        return self._format_movies(filtered.head(top_n))

    def latest_by_genre(self, genre, min_votes=30, top_n=20):
        mask = self.df['genres_str'].str.contains(genre, case=False, na=False)
        filtered = self.df[mask].copy()
        filtered = filtered[filtered['vote_count'] >= min_votes]
        filtered = filtered[filtered['release_year'] >= 2010]
        filtered = filtered.sort_values('release_year', ascending=False)
        return self._format_movies(filtered.head(top_n))

    def multi_genre_search(self, genres, min_votes=50, sort_by='vote_average', top_n=20):
        if not genres:
            return self._format_movies(self.df.head(0))
        mask = pd.Series(True, index=self.df.index)
        for genre in genres:
            mask &= self.df['genres_str'].str.contains(genre, case=False, na=False)
        filtered = self.df[mask].copy()
        filtered = filtered[filtered['vote_count'] >= min_votes]
        if sort_by == 'vote_average':
            filtered = filtered.sort_values('vote_average', ascending=False)
        else:
            filtered = filtered.sort_values('popularity', ascending=False)
        return self._format_movies(filtered.head(top_n))

    def underrated_gems(self, genre, max_votes=500, min_votes=20, top_n=15):
        mask = self.df['genres_str'].str.contains(genre, case=False, na=False)
        filtered = self.df[mask].copy()
        filtered = filtered[(filtered['vote_count'] >= min_votes) & (filtered['vote_count'] <= max_votes) & (filtered['vote_average'] >= 6.5)]
        filtered = filtered.sort_values('vote_average', ascending=False)
        return self._format_movies(filtered.head(top_n))

    def genre_stats(self, genre):
        mask = self.df['genres_str'].str.contains(genre, case=False, na=False)
        genre_df = self.df[mask]
        return {
            'total_movies': len(genre_df),
            'avg_rating': round(genre_df['vote_average'].mean(), 2),
            'avg_popularity': round(genre_df['popularity'].mean(), 2),
            'top_rated': genre_df.loc[genre_df['vote_count'] >= 100].sort_values('vote_average', ascending=False).iloc[0]['title'] if len(genre_df) > 0 else 'N/A',
            'most_popular': genre_df.sort_values('popularity', ascending=False).iloc[0]['title'] if len(genre_df) > 0 else 'N/A',
            'year_range': f"{int(genre_df['release_year'].min())} - {int(genre_df['release_year'].max())}" if len(genre_df) > 0 else 'N/A'
        }

    def _format_movies(self, filtered_df):
        movies = []
        for _, row in filtered_df.iterrows():
            movies.append({
                'title': row['title'],
                'genres': row['genres_str'],
                'overview': row['overview'][:300] if pd.notna(row['overview']) and row['overview'] else '',
                'vote_average': float(row['vote_average']),
                'vote_count': int(row['vote_count']),
                'popularity': float(row['popularity']),
                'release_year': int(row['release_year']) if pd.notna(row['release_year']) else 0
            })
        return movies
