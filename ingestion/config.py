# ingestion/config.py
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data paths
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "books.db")

# Input paths
# Place your CSV files in a 'data/raw' folder or update this path
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
DEFAULT_CSV_PATH = os.path.join(RAW_DATA_DIR, "books_input.csv")

# OpenLibrary API Settings
OPENLIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
SUBJECTS_TO_FETCH = ["science_fiction", "love", "mystery", "programming"]
