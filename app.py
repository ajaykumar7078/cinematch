"""Streamlit web interface - Movie Recommendation System."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
import pandas as pd
from src.data_loader import load_movies, get_movie_by_title, get_all_titles, get_all_genre_names
from src.recommender import ContentBasedRecommender
from src.genre_explorer import GenreExplorer

st.set_page_config(page_title="Movie Recommender Pro", page_icon="🎬", layout="wide")
st.markdown("""<style>.main-header{font-size:2.5rem;font-weight:800}.movie-card{background:#1a1a2e;border-radius:12px;padding:1rem;margin-bottom:0.8rem;border:1px solid #2a2a4e}.movie-card:hover{border-color:#e94560}.movie-genre{display:inline-block;background:#e94560;color:white;padding:2px 8px;border-radius:12px;font-size:0.7rem;margin-right:4px}.rating-badge{display:inline-flex;align-items:center;background:#f0c040;color:#1a1a2e;padding:2px 10px;border-radius:20px;font-weight:700}</style>""", unsafe_allow_html=True)

@st.cache_resource
def load_all():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'tmdb_5000_movies.csv.gz')
    df = load_movies(data_path)
    rec = ContentBasedRecommender(max_features=8000)
    rec.fit(df)
    explorer = GenreExplorer(df)
    genres = get_all_genre_names(df)
    titles = get_all_titles(df)
    return df, rec, explorer, genres, titles

with st.spinner("Loading 4,800+ movies..."):
    df, recommender, explorer, ALL_GENRES, ALL_TITLES = load_all()

with st.sidebar:
    st.markdown("# 🎬 Movie Pro")
    st.caption("v2.0")
    mode = st.radio("Mode", ["🎯 Similar Movies", "🔍 Genre Explorer", "🎭 Multi-Genre", "💎 Hidden Gems", "📊 Genre Stats"], index=0, label_visibility="collapsed")
    st.markdown(f"📊 **{len(df):,} movies** · 🏷️ {len(ALL_GENRES)} genres")

def render_card(movie, show_score=False, rank=None):
    genres_html = " ".join(f'<span class="movie-genre">{g.strip()}</span>' for g in movie['genres'].split('|') if g.strip())
    score = f'<span class="rating-badge" style="background:#e94560">🔗 {movie["similarity_score"]*100:.0f}%</span>' if show_score and movie.get('similarity_score') else ''
    rank_html = f'<span style="font-size:1.2rem;font-weight:700;color:#e94560;margin-right:8px">#{rank}</span>' if rank else ''
    overview = (movie.get('overview','')[:200] + '...') if len(movie.get('overview','')) > 200 else movie.get('overview','')
    return f'<div class="movie-card"><div style="display:flex;justify-content:space-between"><div>{rank_html}<b>{movie["title"]}</b> <span style="color:#888">({movie["release_year"]})</span></div><div>{score}<span class="rating-badge">⭐ {movie["vote_average"]:.1f}</span></div></div><div>{genres_html}</div><div style="color:#aaa;font-size:0.85rem;margin-top:6px">{overview}</div></div>'

if mode == "🎯 Similar Movies":
    st.markdown('<p class="main-header">🎯 Similar Movie Finder</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([3,1])
    with col1: search_term = st.text_input("Search movie:")
    with col2: top_n = st.number_input("Count:", 3, 30, 10)
    if search_term:
        matches = [t for t in ALL_TITLES if search_term.lower() in t.lower()]
        if matches:
            selected = st.selectbox("Did you mean?", matches)
            movie = get_movie_by_title(df, selected)
            if movie:
                st.markdown(f"**{movie['title']}** · 🏷️ {movie['genres_str']} · ⭐ {movie['vote_average']}/10")
                st.caption(movie['overview'][:300])
            if st.button("🎯 Get Similar", type="primary"):
                with st.spinner("Computing..."):
                    results = recommender.recommend(df, selected, top_n=top_n)
                    if results:
                        for i, rec in enumerate(results, 1):
                            st.markdown(render_card(rec, show_score=True, rank=i), unsafe_allow_html=True)

elif mode == "🔍 Genre Explorer":
    st.markdown('<p class="main-header">🔍 Genre Explorer</p>', unsafe_allow_html=True)
    selected_genre = st.selectbox("Genre:", ALL_GENRES, index=ALL_GENRES.index("Thriller"))
    sort_mode = st.selectbox("Sort:", ["Top Rated", "Most Popular", "Latest"])
    count = st.number_input("Show:", 5, 50, 20)
    sort = {"Top Rated":"top","Most Popular":"popular","Latest":"latest"}[sort_mode]
    fn = {"top": explorer.top_by_genre, "popular": explorer.popular_by_genre, "latest": explorer.latest_by_genre}[sort]
    results = fn(selected_genre, top_n=count)
    stats = explorer.genre_stats(selected_genre)
    ca, cb, cc, cd = st.columns(4)
    ca.metric("Movies", stats['total_movies']); cb.metric("Avg Rating", stats['avg_rating']); cc.metric("Years", stats['year_range']); cd.metric("Top", stats['top_rated'][:12])
    if results:
        for i, m in enumerate(results, 1):
            st.markdown(render_card(m, rank=i), unsafe_allow_html=True)

elif mode == "🎭 Multi-Genre":
    st.markdown('<p class="main-header">🎭 Multi-Genre Search</p>', unsafe_allow_html=True)
    selected_genres = st.multiselect("Genres (ALL):", ALL_GENRES, default=["Horror","Thriller"])
    if selected_genres:
        results = explorer.multi_genre_search(selected_genres, top_n=20)
        if results:
            for i, m in enumerate(results, 1):
                st.markdown(render_card(m, rank=i), unsafe_allow_html=True)

elif mode == "💎 Hidden Gems":
    st.markdown('<p class="main-header">💎 Hidden Gems</p>', unsafe_allow_html=True)
    gem_genre = st.selectbox("Genre:", ALL_GENRES, index=ALL_GENRES.index("Horror"))
    results = explorer.underrated_gems(gem_genre, top_n=15)
    if results:
        for i, m in enumerate(results, 1):
            st.markdown(render_card(m, rank=i), unsafe_allow_html=True)

elif mode == "📊 Genre Stats":
    st.markdown('<p class="main-header">📊 Genre Stats</p>', unsafe_allow_html=True)
    stats_data = [{"Genre": g, "Movies": explorer.genre_stats(g)['total_movies'], "Avg Rating": explorer.genre_stats(g)['avg_rating'], "Top": explorer.genre_stats(g)['top_rated']} for g in ALL_GENRES]
    sdf = pd.DataFrame(stats_data).sort_values("Movies", ascending=False)
    st.dataframe(sdf, use_container_width=True, hide_index=True)
    st.bar_chart(sdf.set_index("Genre")["Movies"])
