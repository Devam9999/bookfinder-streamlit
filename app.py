import streamlit as st
import sys
import os

# Add the parent directory to sys.path to resolve 'storage' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- CONFIGURATION ---
st.set_page_config(page_title="Book Finder", page_icon="📚", layout="wide")

# --- CUSTOM CSS LOADING ---
def load_css_content(file_name):
    with open(file_name) as f:
        return f.read()

css_files = ['main.css', 'header.css', 'components.css', 'footer.css', 'pipeline.css', 'home.css']
combined_css = ""
for css_file in css_files:
    combined_css += load_css_content(os.path.join('assets', 'css', css_file))

st.markdown(f'<style>{combined_css}</style>', unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'page' not in st.session_state:
    st.session_state.page = "Home"

if 'view' not in st.session_state:
    st.session_state.view = 'list'
if 'selected_book' not in st.session_state:
    st.session_state.selected_book = None
if 'query' not in st.session_state:
    st.session_state.query = ""

def set_page(page_name):
    st.session_state.page = page_name

# --- IMPORTS ---
from components.header import render_header
from components.footer import render_footer
from views.home import render_home
from views.how_it_works import render_how_it_works
from views.data_insights import render_data_insights
from views.about import render_about

# --- LAYOUT ---

# 1. Header
render_header(set_page)

# Inject styling for nav buttons based on state
st.markdown(f"""
<style>
    /* Dynamic Active State Styling */
    div[data-testid="stHorizontalBlock"] button[title="Home"] {{
        color: {"#f0f6fc" if st.session_state.page == "Home" else "#8b949e"} !important;
    }}
    
    /* Apply Link Style to text buttons */
    div[data-testid="column"] button {{
        background: transparent;
        border: none;
        color: #8b949e;
    }}
</style>
""", unsafe_allow_html=True)

# 2. Main Content Routing
page = st.session_state.page

if page == "Home":
    render_home()
elif page == "How It Works":
    render_how_it_works()
elif page == "Data Insights":
    render_data_insights()
elif page == "About":
    render_about()

# 3. Footer
render_footer()
