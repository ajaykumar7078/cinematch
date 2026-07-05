"""Data loader for the TMDB 5000 Movie Dataset."""
import json, gzip
import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'tmdb_5000_movies.csv.gz')

def load_movies(path=None):
    if path is None:
        path = DATA_PATH
    if path.endswith('.gz'):
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            df = pd.read_csv(f)
    else:
        df = pd.read_csv(path)
    df['genres_list'] = df['genres'].apply(_parse_genres)
    df['keywords_list'] = df['keywords'].apply(_parse_keywords)
    df['genres_str'] = df['genres_list'].apply(lambda g: '|'.join(g) if g else '')
    df['overview'] = df['overview'].fillna('')
    df['combined_features'] = (
        df['genres_str'].str.replace('|', ' ') + ' ' +
        df['overview'] + ' ' +
        df['keywords_list'].apply(lambda k: ' '.join(k) if k else '')
    )
    df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year.fillna(0).astype(int)
    return df

def _parse_genres(genres_json):
    try:
        genres = json.loads(genres_json) if isinstance(genres_json, str) else genres_json
        return [g['name'] for g in genres] if genres else []
    except:
        return []

def _parse_keywords(keywords_json):
    try:
        keywords = json.loads(keywords_json) if isinstance(keywords_json, str) else keywords_json
        return [k['name'] for k in keywords] if keywords else []
    except:
        return []

def get_movie_by_title(df, title):
    match = df[df['title'].str.lower() == title.lower()]
    if match.empty:
        match = df[df['title'].str.lower().str.contains(title.lower(), na=False)]
    return match.iloc[0] if not match.empty else None

def get_all_titles(df):
    return sorted(df['title'].tolist())

def get_movies_by_genre(df, genre_name, min_votes=50, sort_by='vote_average'):
    mask = df['genres_str'].str.contains(genre_name, case=False, na=False)
    filtered = df[mask]
    filtered = filtered[filtered['vote_count'] >= min_votes]
    if sort_by == 'vote_average':
        filtered = filtered.sort_values('vote_average', ascending=False)
    else:
        filtered = filtered.sort_values('popularity', ascending=False)
    return filtered

def get_all_genre_names(df):
    all_genres = set()
    for genres_str in df['genres_str']:
        for g in genres_str.split('|'):
            if g:
                all_genres.add(g)
    return sorted(all_genres)
