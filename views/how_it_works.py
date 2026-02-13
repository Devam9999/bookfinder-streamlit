import streamlit as st

def render_how_it_works():
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">Book Recommendation Pipeline</div>
            <div class="hero-subtitle">From raw data crawls to semantic AI — a detailed breakdown of our ETL and retrieval architecture.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 📊 Data Engineering Pipeline (ETL)")
    st.write("")
    
    # Step 1: Data Ingestion
    st.markdown("""
    <div class="pipeline-step">
        <div class="step-header">
            <div class="step-icon-badge">1️⃣</div>
            <div class="step-title-block">
                <h3>Web Crawling (Ingestion)</h3>
                <p>Fetching book metadata from Open Library and other literary databases.</p>
            </div>
        </div>
        <div class="step-content">
            <ul>
                <li>Query <strong>Open Library API</strong> for book metadata (title, author, ISBN, description)</li>
                <li>Fetch static and discovered dynamically indexed via direct book lookups</li>
                <li>Store high-quality, well-documented faculty and avoid web-site duplicates</li>
            </ul>
        </div>
        <div class="why-matters">
            <span class="why-matters-label">Why it matters:</span>
            <p>Gathering metadata at scale is the raw data layer — crawling via the Open API enables repeatable and extensible book strategy.</p>
        </div>
        <div class="tech-badges">
            <span class="tech-badge">Python</span>
            <span class="tech-badge">Requests</span>
            <span class="tech-badge">OpenLibrary API</span>
            <span class="tech-badge">CSV Processing</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Connector
    st.markdown('<div class="pipeline-connector"></div>', unsafe_allow_html=True)
    
    # Step 2: Data Transformation
    st.markdown("""
    <div class="pipeline-step">
        <div class="step-header">
            <div class="step-icon-badge">2️⃣</div>
            <div class="step-title-block">
                <h3>Data Transformation</h3>
                <p>Cleaning, normalizing, and deduplicating raw book data.</p>
            </div>
        </div>
        <div class="step-content">
            <ul>
                <li>Parse and <strong>normalize</strong> fields into uniform schema (Title, Author, Genre, Description)</li>
                <li>Remove HTML artifacts and standardize text encoding</li>
                <li>Deduplicate books using <strong>ISBN matching</strong> and fuzzy title/author comparison</li>
                <li>Enrich data quality by filling missing genres via keyword extraction</li>
            </ul>
        </div>
        <div class="why-matters">
            <span class="why-matters-label">Why it matters:</span>
            <p>Even the singularise subject will hurt LLM embeddings and retrieval accuracy.</p>
        </div>
        <div class="tech-badges">
            <span class="tech-badge">Pandas</span>
            <span class="tech-badge">NumPy</span>
            <span class="tech-badge">Data Cleaner Module</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Connector
    st.markdown('<div class="pipeline-connector"></div>', unsafe_allow_html=True)
    
    # Step 3: Embedding Generation
    st.markdown("""
    <div class="pipeline-step">
        <div class="step-header">
            <div class="step-icon-badge">3️⃣</div>
            <div class="step-title-block">
                <h3>Profile-Level Embedding</h3>
                <p>Converting book descriptions into semantic vector representations.</p>
            </div>
        </div>
        <div class="step-content">
            <ul>
                <li>Combine <strong>title + description + genre</strong> into rich text profiles</li>
                <li>Generate 384-dimensional embeddings using <strong>Sentence-BERT (all-MiniLM-L6-v2)</strong></li>
                <li>Store embeddings alongside book IDs for fast similarity search</li>
                <li>Batch processing optimization to handle large-scale encoding efficiently</li>
            </ul>
        </div>
        <div class="why-matters">
            <span class="why-matters-label">Why it matters:</span>
            <p>Using SBERT, we go beyond bag-of-words — enabling AI to understand thematic similarity not just keyword overlap.</p>
        </div>
        <div class="tech-badges">
            <span class="tech-badge">Sentence-Transformers</span>
            <span class="tech-badge">all-MiniLM-L6-v2</span>
            <span class="tech-badge">PyTorch</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Connector
    st.markdown('<div class="pipeline-connector"></div>', unsafe_allow_html=True)
    
    # Step 4: Vector Storage
    st.markdown("""
    <div class="pipeline-step">
        <div class="step-header">
            <div class="step-icon-badge">4️⃣</div>
            <div class="step-title-block">
                <h3>Storage (SQLite + Vectors)</h3>
                <p>Persisting metadata and embeddings for retrieval operations.</p>
            </div>
        </div>
        <div class="step-content">
            <ul>
                <li><strong>SQLite database</strong> stores structured metadata (title, author, ISBN, genre, description)</li>
                <li><strong>Pickle/JSON serialization</strong> stores dense embeddings</li>
                <li>Indexed ID-based lookup enables O(1) book metadata retrieval</li>
                <li>Efficient caching to avoid re-embedding unchanged book profiles</li>
            </ul>
        </div>
        <div class="why-matters">
            <span class="why-matters-label">Why it matters:</span>
            <p>Fast vector search and metadata availability are paramount for real-time AI-driven matching.</p>
        </div>
        <div class="tech-badges">
            <span class="tech-badge">SQLite</span>
            <span class="tech-badge">Pickle</span>
            <span class="tech-badge">JSON</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Connector
    st.markdown('<div class="pipeline-connector"></div>', unsafe_allow_html=True)
    
    # Step 5: Semantic Search
    st.markdown("""
    <div class="pipeline-step">
        <div class="step-header">
            <div class="step-icon-badge">5️⃣</div>
            <div class="step-title-block">
                <h3>Semantic Search (Retrieval)</h3>
                <p>Real-time query embedding and similarity-based book ranking.</p>
            </div>
        </div>
        <div class="step-content">
            <ul>
                <li>User query is <strong>embedded</strong> using the same SBERT model</li>
                <li><strong>Cosine similarity</strong> computed between query vector and all book embeddings</li>
                <li>Top-K most similar books retrieved and ranked by similarity score</li>
                <li>Deduplication applied to ensure no repeated books in results</li>
                <li>Results displayed with match percentage for transparency</li>
            </ul>
        </div>
        <div class="why-matters">
            <span class="why-matters-label">Why it matters:</span>
            <p>Semantic matching lets users search like "a gripping mystery set in Victorian London" — not just exact titles or authors.</p>
        </div>
        <div class="tech-badges">
            <span class="tech-badge">Scikit-Learn</span>
            <span class="tech-badge">Cosine Similarity</span>
            <span class="tech-badge">NumPy</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Why This Pipeline Matters
    st.markdown("---")
    st.markdown("""
    <div class="architecture-matters">
        <h2>🎯 Why This Pipeline Architecture Matters</h2>
        <ul>
            <li><strong>Scalability:</strong> Modular ETL allows adding new data sources (Goodreads, Amazon) without rearchitecting</li>
            <li><strong>Accuracy:</strong> SBERT embeddings capture semantic meaning far better than keyword search</li>
            <li><strong>Speed:</strong> Pre-computed embeddings enable sub-second query responses even with 10,000+ books</li>
            <li><strong>Transparency:</strong> Similarity scores show users why each book was recommended</li>
            <li><strong>Maintainability:</strong> Clean separation between ingestion, transformation, storage, and retrieval</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
