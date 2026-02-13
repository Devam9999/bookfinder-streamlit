import streamlit as st
import numpy as np
import os
import sys

# Ensure storage module can be found if needed, though app.py usually handles sys.path
# But imports should work if running from root
from storage.db import get_recent_books, get_database_stats, get_books_by_ids, get_book_ids_by_genres
from transformation.embedder import load_model, load_embeddings
from sklearn.metrics.pairwise import cosine_similarity

# --- RESOURCE LOADING ---
@st.cache_resource
def load_search_resources():
    try:
        model = load_model()
        embeddings_data = load_embeddings()
        return model, embeddings_data
    except Exception as e:
        return None, None

model, embeddings_data = load_search_resources()

def semantic_search(query_text, top_k=5):
    if not embeddings_data or not model: return [], []
    
    # 1. Hard Genre Filtering
    query_lower = query_text.lower()
    
    # Map common keywords to DB genre substrings
    genre_keywords = {
        "thriller": ["thriller", "suspense", "mystery", "crime"],
        "mystery": ["mystery", "crime", "detective", "thriller"],
        "romance": ["romance", "love"],
        "scifi": ["sci-fi", "science fiction", "futuristic", "space"],
        "science fiction": ["sci-fi", "science fiction"],
        "fantasy": ["fantasy", "magic"],
        "history": ["history", "biography", "historical"],
        "biography": ["biography", "memoir"],
        "horror": ["horror", "scary"],
        "psychological": ["psychological", "thriller"],
        "programming": ["programming", "code", "software", "computer"],
        "tech": ["technology", "computer"],
    }
    
    target_genres = set()
    for keyword, mapped_genres in genre_keywords.items():
        if keyword in query_lower:
            target_genres.update(mapped_genres)
            
    candidate_indices = None
    all_ids = np.array(embeddings_data['ids'])
    
    if target_genres:
        # Fetch matching IDs from DB
        filtered_ids_list = get_book_ids_by_genres(list(target_genres))
        if not filtered_ids_list:
             # Strict filtering: if genre keywords present but no books match, return empty
             # Or could fallback, but user requested "restrict".
             return [], []
             
        valid_ids_set = set(filtered_ids_list)
        # Find indices of these IDs in the embedding matrix
        # This mask approach fits into memory for typical catalog sizes
        mask = [bid in valid_ids_set for bid in all_ids]
        if not any(mask):
            return [], []
        
        candidate_indices = np.where(mask)[0]
        candidate_embeddings = embeddings_data['embeddings'][candidate_indices]
        candidate_ids = all_ids[candidate_indices]
    else:
        candidate_embeddings = embeddings_data['embeddings']
        candidate_ids = all_ids

    # 2. Normalize Query & Compute Similarity
    # normalize_embeddings=True ensures query is unit vector
    query_embedding = model.encode([query_text], normalize_embeddings=True)
    
    # Cosine similarity on normalized vectors = Dot product
    # But sklearn cosine_similarity handles it generally
    scores = cosine_similarity(query_embedding, candidate_embeddings)[0]
    
    # 3. Rank
    top_k_indices = np.argsort(scores)[::-1][:top_k]
    return candidate_ids[top_k_indices].tolist(), scores[top_k_indices]

# --- HELPER FUNCTIONS ---
def view_book_details(book):
    st.session_state.selected_book = book
    st.session_state.view = 'detail'

def go_back():
    st.session_state.view = 'list'
    st.session_state.selected_book = None
    # Ensure query persists

def update_query():
    st.session_state.query = st.session_state.search_input

def search_by_genre(genre):
    """Trigger search for a specific genre"""
    st.session_state.query = f"{genre} books"

# --- MAIN RENDERER ---
def render_home():
    if st.session_state.view == 'detail':
        # --- DETAIL PAGE ---
        book = st.session_state.selected_book
        if book:
            st.button("← Back to Search", on_click=go_back)
            
            st.markdown(f"## {book.get('title')}")
            
            col_img, col_info = st.columns([1, 2])
            with col_img:
                if book.get('cover_image'):
                     st.image(book['cover_image'], use_container_width=True)
                else:
                     st.markdown(f"<div style='height:400px; background-color:#21262d; display:flex; align-items:center; justify-content:center; border-radius:12px; font-size:80px;'>📕</div>", unsafe_allow_html=True)

            with col_info:
                st.markdown(f"**Author:** {book.get('author') or 'Unknown'}")
                st.markdown(f"**Published:** {book.get('publish_year')} | **ISBN:** {book.get('isbn') or 'N/A'}")
                st.markdown(f"**Genre:** {book.get('genre')}")
                
                st.markdown("#### Abstract")
                st.write(book.get('description') or "No description available.")
                
                st.markdown("---")
                st.caption(f"Source ID: {book.get('id')}")
            
    else:
        # --- LIST PAGE (HERO & SEARCH) ---
        
        # Hero Section
        if not st.session_state.query:
            st.markdown("""
                <div class="hero-container">
                    <div class="hero-title">Discover Your Next Read</div>
                    <div class="hero-subtitle">Semantic search powered by AI. Describe the vibe, plot, or character you're looking for.</div>
                </div>
            """, unsafe_allow_html=True)

        # Search Bar
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            query = st.text_input(
                "", 
                placeholder="e.g., 'A mystery novel set in Victorian London'...", 
                label_visibility="collapsed",
                key="search_input",
                value=st.session_state.query,
                on_change=update_query
            )
        
        st.write("") # Spacer

        # Only show home content when no search query
        if not st.session_state.query:
            # Stats Widgets
            stats = get_database_stats()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{stats.get('total_books', 0)}</div>
                    <div class="metric-label">Total Books</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{stats.get('total_genres', 0)}</div>
                    <div class="metric-label">Explore Genres</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{stats.get('total_authors', 0)}</div>
                    <div class="metric-label">Featured Authors</div>
                </div>
                """, unsafe_allow_html=True)
            # Featured Books Section
            st.markdown("""
            <div class="featured-section">
                <h2 class="featured-title">Featured Books</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Get random recent books as "featured"
            recent_books = get_recent_books(limit=4)
            if recent_books:
                cols = st.columns(4)
                for i, book in enumerate(recent_books):
                    with cols[i]:
                        with st.container(border=True):
                            if book.get('cover_image'):
                                try:
                                    st.markdown(f"""
                                    <div style="height:280px; width:100%; overflow:hidden; border-radius:8px; margin-bottom:10px;">
                                        <img src="{book['cover_image']}" style="width:100%; height:100%; object-fit:cover; object-position:top;">
                                    </div>
                                    """, unsafe_allow_html=True)
                                except:
                                    st.markdown("<div style='height:280px; background:#21262d; border-radius:8px; margin-bottom:10px;'></div>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<div style='height:280px; background-color:#21262d; color:#8b949e; display:flex; align-items:center; justify-content:center; border-radius:8px; margin-bottom:10px; font-size:3rem;'>📚</div>", unsafe_allow_html=True)
                            
                            st.markdown(f"""
                                <div style="flex-grow:1;">
                                    <div class="title-text" title="{book.get('title')}">{book.get('title')[:40]}...</div>
                                    <div class="author-text">{book.get('author') or 'Unknown'}</div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            st.button("View Details", key=f"featured_{book['id']}", on_click=view_book_details, args=(book,))
            
            # Trending Genres Section
            st.write("")
            st.markdown("""
            <div class="featured-section">
                <h2 class="featured-title">📖 Trending Genres</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")  # Small spacing
            genres = ["Mystery", "Science Fiction", "Romance", "Fantasy", "Thriller", "Historical Fiction", "Horror", "Biography"]
            genre_cols = st.columns(4)
            for i, genre in enumerate(genres):
                with genre_cols[i % 4]:
                    st.button(genre, key=f"genre_{genre}", on_click=search_by_genre, args=(genre,), use_container_width=True)
            
            # Call to Action
            st.write("")
            st.write("")
            st.markdown("""
            <div class="cta-section">
                <h3 class="cta-title">🚀 Start Your Reading Journey</h3>
                <p class="cta-text">Use the search bar above to describe the kind of book you're looking for. Our AI will find the perfect match!</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.write("") # Spacer

        if st.session_state.query:
            query = st.session_state.query
            
            # Search Header with Clear Button
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.markdown(f"### Results for '{query}'")
            with col2:
                if st.button("Clear Search", key="clear_search", type="secondary", use_container_width=True):
                    st.session_state.query = ""
                    st.rerun()
            st.markdown("---")
            
            if embeddings_data and model:
                with st.spinner("Analyzing semantic meaning..."):
                    limit = 8
                    # Fetch 3x candidates to ensure enough unique results after dedup
                    ids, scores = semantic_search(query, top_k=limit * 3)
                
                if ids:
                    st.markdown(f"##### Best Matches")
                    # Books Fetch
                    books = get_books_by_ids(ids)
                    book_map = {b['id']: b for b in books}
                    ordered_books = [book_map[id] for id in ids if id in book_map]

                    # De-dup logic
                    seen_isbns = set()
                    seen_titles = set()
                    unique_books = []
                    unique_scores = []

                    for b, s in zip(ordered_books, scores):
                        if len(unique_books) >= limit: break # Stop once we have enough
                        
                        isbn = b.get('isbn')
                        t = (b.get('title') or "").lower().strip()
                        a = (b.get('author') or "").lower().strip()
                        key = (t,a)
                        if isbn and isbn in seen_isbns: continue
                        if key in seen_titles: continue
                        if isbn: seen_isbns.add(isbn)
                        if t: seen_titles.add(key)
                        unique_books.append(b)
                        unique_scores.append(s)

                    # Grid Render
                    # Use batching to ensure rows are aligned (grid) instead of masonry (columns)
                    batch_size = 4
                    results = list(zip(unique_books, unique_scores))
                    
                    for i in range(0, len(results), batch_size):
                        batch = results[i:i + batch_size]
                        cols = st.columns(batch_size)
                        
                        for j, (book, score) in enumerate(batch):
                            with cols[j]:
                                with st.container(border=True): # Uses card css
                                    # Image
                                    if book.get('cover_image'):
                                        try:
                                            st.markdown(f"""
                                            <div style="height:280px; width:100%; overflow:hidden; border-radius:8px; margin-bottom:10px;">
                                                <img src="{book['cover_image']}" style="width:100%; height:100%; object-fit:cover; object-position:top;">
                                            </div>
                                            """, unsafe_allow_html=True)
                                        except:
                                            st.markdown("<div style='height:280px; background:#21262d; border-radius:8px; margin-bottom:10px;'></div>", unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"<div style='height:280px; background-color:#21262d; color:#8b949e; display:flex; align-items:center; justify-content:center; border-radius:8px; margin-bottom:10px;'>{book.get('title')[:15]}...</div>", unsafe_allow_html=True)
                                    
                                    # Content Container for alignment - Fixed Height for Text
                                    st.markdown(f"""
                                        <div style="flex-grow:1; min-height: 120px;">
                                            <div class="title-text" style="height: 48px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;" title="{book.get('title')}">{book.get('title')}</div>
                                            <div class="author-text" style="height: 24px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{book.get('author') or 'Unknown'}</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                                    
                                    match_color = "#238636" if score > 0.5 else "#d29922"
                                    st.markdown(f"<span style='color:{match_color}; font-size:0.8rem'>● Match {score:.0%}</span>", unsafe_allow_html=True)
                                    
                                    st.button("View Details", key=f"btn_{book['id']}", on_click=view_book_details, args=(book,))
                else:
                    st.warning("No matches found.")
            else:
                 st.error("Embeddings not loaded.")
