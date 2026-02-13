import streamlit as st
from storage.db import get_database_stats

def render_data_insights():
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">Book Data Insights</div>
            <div class="hero-subtitle">How book composition, data completeness, and text richness influence semantic retrieval and AI-driven recommendations.</div>
        </div>
    """, unsafe_allow_html=True)
    
    stats = get_database_stats()
    
    # Book Collection Landscape Section
    st.markdown("## 📊 Book Collection Landscape")
    st.write("")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="landscape-card">
            <h4>📖 Core Collection Backbone</h4>
            <ul>
                <li>Classic Literature</li>
                <li>Contemporary Fiction</li>
            </ul>
            <p style="margin-top:12px;">Primary source of long-term reader engagement and high-confidence recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="landscape-card">
            <h4>🔬 Genre & Niche Strength</h4>
            <ul>
                <li>Science Fiction</li>
                <li>Mystery & Thriller</li>
            </ul>
            <p style="margin-top:12px;">Adds specialized expertise for niche queries, reducing uncertainty in genre-specific recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="landscape-card">
            <h4>🌍 International Diversity</h4>
            <ul>
                <li>Global Authors</li>
                <li>Translated Works</li>
            </ul>
            <p style="margin-top:12px;">High-value global exposure, but limited data depth impacts semantic matching.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Data Quality & AI Risk Section
    st.markdown("---")
    st.markdown("## ⚠️ Data Quality & AI Risk Assessment")
    st.write("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="risk-panel risk-high">
            <h4>Descriptions</h4>
            <span class="risk-badge badge-high">High Risk</span>
            <p style="margin-top:12px;">While descriptions exist severely degrade semantic similarity and matching accuracy.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="risk-panel risk-medium">
            <h4>Publication Metadata</h4>
            <span class="risk-badge badge-medium">Medium Risk</span>
            <p style="margin-top:12px;">Limits authority signals and topic confidence scoring.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="risk-panel risk-medium">
            <h4>Genre Classification</h4>
            <span class="risk-badge badge-medium">Medium Risk</span>
            <p style="margin-top:12px;">Affects the alignment of thematic expertise with reader preferences.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="risk-panel risk-low">
            <h4>Author & Title Data</h4>
            <span class="risk-badge badge-low">Low Risk</span>
            <p style="margin-top:12px;">Missing effect on AI ranking; mainly impacts user completeness.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Warning Banner
    st.markdown("""
    <div class="warning-banner">
        <span style="font-size:1.5rem;">⚠️</span>
        <p><strong>Critical:</strong> Missing description content is the single biggest bottleneck preventing high-precision semantic matching.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # NLP Readiness Section
    st.markdown("---")
    st.markdown("## 🧠 NLP Readiness of Text Fields")
    st.write("")
    
    # Descriptions
    st.markdown("""
    <div class="readiness-item">
        <div class="readiness-header">
            <span class="readiness-title">Descriptions</span>
            <span class="readiness-level">Very High</span>
        </div>
        <div class="custom-progress-bar">
            <div class="progress-fill progress-very-high" style="width: 92%;"></div>
        </div>
        <p class="readiness-description">Most valuable field — extremely rich, paragraph-form text with thematic depth.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Genres
    st.markdown("""
    <div class="readiness-item">
        <div class="readiness-header">
            <span class="readiness-title">Genres</span>
            <span class="readiness-level">High</span>
        </div>
        <div class="custom-progress-bar">
            <div class="progress-fill progress-high" style="width: 78%;"></div>
        </div>
        <p class="readiness-description">Good categorical grounding for thematic matching.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Titles
    st.markdown("""
    <div class="readiness-item">
        <div class="readiness-header">
            <span class="readiness-title">Titles</span>
            <span class="readiness-level">Medium</span>
        </div>
        <div class="custom-progress-bar">
            <div class="progress-fill progress-medium" style="width: 55%;"></div>
        </div>
        <p class="readiness-description">Helpful for named references, weaker for thematic depth.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Authors
    st.markdown("""
    <div class="readiness-item">
        <div class="readiness-header">
            <span class="readiness-title">Authors</span>
            <span class="readiness-level">Low</span>
        </div>
        <div class="custom-progress-bar">
            <div class="progress-fill progress-low" style="width: 28%;"></div>
        </div>
        <p class="readiness-description">Sparse data severely limits semantic recall.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Impact on AI Recommendations Section
    st.markdown("---")
    st.markdown("""
    <div class="impact-section">
        <h3>💡 Impact on AI Book Recommendations</h3>
        <ul>
            <li>Books with strong descriptions text dominate top rankings</li>
            <li>Missing thematic sections reduce ranking confidence</li>
            <li>Genre-heavy profiles introduce uncertainty in cross-genre recommendations</li>
            <li>Improving text completeness directly boosts LLM matching quality</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Additional Statistics
    st.markdown("---")
    st.markdown("## 📊 Collection Statistics")
    st.write("")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="text-align:center; padding:24px; background-color:#161b22; border-radius:12px; border:1px solid #30363d;">
            <div style="font-size:2.5rem; font-weight:800; color:#2ea043; margin-bottom:8px;">{stats.get('total_books', 0):,}</div>
            <div style="color:#8b949e; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px;">Total Books</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align:center; padding:24px; background-color:#161b22; border-radius:12px; border:1px solid #30363d;">
            <div style="font-size:2.5rem; font-weight:800; color:#3b82f6; margin-bottom:8px;">{stats.get('total_genres', 0)}</div>
            <div style="color:#8b949e; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px;">Unique Genres</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="text-align:center; padding:24px; background-color:#161b22; border-radius:12px; border:1px solid #30363d;">
            <div style="font-size:2.5rem; font-weight:800; color:#a855f7; margin-bottom:8px;">{stats.get('total_authors', 0):,}</div>
            <div style="color:#8b949e; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px;">Contributing Authors</div>
        </div>
        """, unsafe_allow_html=True)
