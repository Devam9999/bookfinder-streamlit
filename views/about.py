import streamlit as st

def render_about():
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">About Book Finder</div>
            <div class="hero-subtitle">AI-Powered Book Recommendation Platform</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Project Overview Section
    st.markdown("## Project Overview")
    st.markdown("""
    Book Finder is an intelligent book recommendation platform designed to bridge the gap between readers and their next favorite book. 
    Using advanced AI techniques, the system enables semantic search that goes beyond traditional keyword matching, enabling meaningful 
    book discovery based on plot, themes, emotions, and narrative style.
    
    This platform addresses the challenge of finding the right book through extensive research profiles to find relevant research mentors. 
    The system intelligently analyzes book descriptions using state-of-the-art NLP models, creating a seamless reading discovery experience.
    """)
    
    # Problem Statement Section
    st.markdown("---")
    st.markdown("## Problem Statement")
    
    with st.container():
        col1, col2 = st.columns([1, 20])
        with col1:
            st.markdown("📌")
        with col2:
            st.markdown("**Information Overload:** Readers often struggle to navigate through vast catalogs to find research mentors, missing community-related expertise.")
    
    with st.container():
        col1, col2 = st.columns([1, 20])
        with col1:
            st.markdown("🔍")
        with col2:
            st.markdown("**Lack of Contextual Search:** Traditional search relies on exact keyword matching, missing semantically related books or books with plot descriptions that don't match the exact keywords.")
    
    with st.container():
        col1, col2 = st.columns([1, 20])
        with col1:
            st.markdown("🎯")
        with col2:
            st.markdown("**Inefficient Matching:** Readers may miss opportunities to discover books with similar narrative styles or thematic expertise aligned with their mood/interest but expressed in different terminology.")
    
    # System Architecture Section
    st.markdown("---")
    st.markdown("## System Architecture")
    
    st.markdown("""
    Book Finder is built on a modular 4-layer architecture that separates concerns and enables seamless data flow:
    """)
    
    # Layer 1: Data Ingestion
    with st.container(border=True):
        st.markdown("### 1. Data Ingestion Layer")
        st.markdown("""
        Responsible for acquiring and loading book data from institutional databases. The system processes unstructured book data into a 
        structured format suitable for further processing and analysis.
        
        **Key Components:**
        - **OpenLibrary Loader:** Fetches book metadata from OpenLibrary API
        - **CSV Loader:** Imports structured book data from various CSV sources
        - **Data Validation:** Ensures data integrity and completeness
        """)
    
    # Layer 2: Transformation Layer
    with st.container(border=True):
        st.markdown("### 2. Transformation Layer")
        st.markdown("""
        Hybrid approach combining NLP (Sentence-BERT) and vector embedding (cosine similarity) converts unstructured research 
        descriptions into machine-readable representations. This approach captures both word meaning and contextual nuances for 
        accurate book-to-query matching.
        
        **Key Components:**
        - **Data Cleaner:** Normalizes and removes duplicates based on ISBN and title/author matching
        - **Embedder:** Generates semantic embeddings using sentence-transformers (All-MiniLM-L6-v2 model)
        """)
    
    # Layer 3: Storage Layer
    with st.container(border=True):
        st.markdown("### 3. Storage Layer")
        st.markdown("""
        Uses a Language Model analysis for the match between semantic query and book profiles, generating human-readable explanations 
        with confidence scores. This approach provides transparent, user-friendly recommendations.
        
        **Key Components:**
        - **SQLite Database:** Stores book metadata including titles, authors, ISBNs, genres, and descriptions
        - **Vector Store:** Persists embeddings for rapid similarity search
        - **Indexing System:** Maintains efficient retrieval mechanisms
        """)
    
    # Layer 4: Presentation Layer
    with st.container(border=True):
        st.markdown("### 4. Presentation Layer")
        st.markdown("""
        Clean, intuitive web interface built with responsive frameworks provides seamless user experience with responsive design 
        and best performance.
        
        **Key Components:**
        - **Streamlit UI:** Modern, responsive interface for search and book discovery
        - **Search Interface:** Real-time semantic search with similarity scoring
        - **Book Detail Views:** Comprehensive book information display
        """)
    
    # Technologies Used Section
    st.markdown("---")
    st.markdown("## Technologies Used")
    
    # Main Technologies (with badges)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align:center; padding:20px; background-color:#161b22; border-radius:12px; margin:10px 0;">
            <div style="font-size:48px; margin-bottom:10px;">🐍</div>
            <h4>Python</h4>
            <p style="color:#8b949e; font-size:0.9rem;">Core programming language</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:20px; background-color:#161b22; border-radius:12px; margin:10px 0;">
            <div style="font-size:48px; margin-bottom:10px;">🎯</div>
            <h4>Streamlit</h4>
            <p style="color:#8b949e; font-size:0.9rem;">Web application framework</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align:center; padding:20px; background-color:#161b22; border-radius:12px; margin:10px 0;">
            <div style="font-size:48px; margin-bottom:10px;">🧠</div>
            <h4>Sentence-BERT</h4>
            <p style="color:#8b949e; font-size:0.9rem;">Semantic embeddings model</p>
        </div>
        """, unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div style="text-align:center; padding:20px; background-color:#161b22; border-radius:12px; margin:10px 0;">
            <div style="font-size:48px; margin-bottom:10px;">📊</div>
            <h4>Scikit-Learn</h4>
            <p style="color:#8b949e; font-size:0.9rem;">Cosine similarity calculations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div style="text-align:center; padding:20px; background-color:#161b22; border-radius:12px; margin:10px 0;">
            <div style="font-size:48px; margin-bottom:10px;">💾</div>
            <h4>SQLite</h4>
            <p style="color:#8b949e; font-size:0.9rem;">Lightweight database for metadata</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown("""
        <div style="text-align:center; padding:20px; background-color:#161b22; border-radius:12px; margin:10px 0;">
            <div style="font-size:48px; margin-bottom:10px;">🔄</div>
            <h4>Pandas</h4>
            <p style="color:#8b949e; font-size:0.9rem;">Data processing and cleaning</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional Technologies
    st.markdown("#### Additional Technologies")
    tech_badges = ["NumPy", "Requests", "Pickle", "JSON", "Docker", "Git"]
    badge_html = " ".join([f'<span style="background:#238636; padding:4px 12px; border-radius:12px; color:white; margin:4px; display:inline-block; font-size:0.85rem;">{tech}</span>' for tech in tech_badges])
    st.markdown(badge_html, unsafe_allow_html=True)
    
    # Key Features Section
    st.markdown("---")
    st.markdown("## Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="padding:10px 0;">
            <h4>✅ Semantic Search Engine</h4>
            <p style="color:#8b949e;">Find books based on meaning, not just keywords</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="padding:10px 0;">
            <h4>✅ AI-Powered Recommendations</h4>
            <p style="color:#8b949e;">Intelligent book matching using transformer models</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="padding:10px 0;">
            <h4>✅ Deduplication Logic</h4>
            <p style="color:#8b949e;">Ensures each book appears only once in search results</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="padding:10px 0;">
            <h4>✅ Real-Time Analytics</h4>
            <p style="color:#8b949e;">Live database statistics and similarity scores</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="padding:10px 0;">
            <h4>✅ Data Transparency</h4>
            <p style="color:#8b949e;">Insights into data quality and collection composition</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="padding:10px 0;">
            <h4>✅ Responsive Design</h4>
            <p style="color:#8b949e;">Modern UI with smooth interactions and animations</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Disclaimer Section
    st.markdown("---")
    st.markdown("""
    > ⚠️ **IMPORTANT**
    >
    > This is an academic project developed for educational and research purposes. The system demonstrates the application of 
    > information retrieval and NLP techniques in book recommendation systems. This platform is not officially affiliated 
    > with any library or publishing institution and should be used as a proof of concept.
    """)
    
    # Project Team Section
    st.markdown("---")
    st.markdown("## Project Team")
    
    col1, col2= st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="text-align:center; padding:30px 20px; background-color:#161b22; border-radius:12px;">
            <div style="font-size:64px; margin-bottom:15px;">👨‍💻</div>
            <h3>Chauhan Aman Satpal</h3>
            <p style="color:#8b949e; font-size:0.9rem;">Data Engineer & AI Specialist</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:30px 20px; background-color:#161b22; border-radius:12px;">
            <div style="font-size:64px; margin-bottom:15px;">👨‍💻</div>
            <h3>Devam Gandhi</h3>
            <p style="color:#8b949e; font-size:0.9rem;">Data Engineer & AI Specialist</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; margin-top:30px;">
        <p style="color:#8b949e; font-size:1.1rem;">Group: <strong style="color:#f0f6fc;">Node Nexus</strong></p>
    </div>
    """, unsafe_allow_html=True)
