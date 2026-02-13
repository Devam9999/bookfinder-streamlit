# run_pipeline.py
import argparse
import logging
import json
import os
from typing import List, Dict, Any

from ingestion.csv_loader import load_csv
from ingestion.openlibrary_loader import load_all_openlibrary_data
from ingestion.config import DEFAULT_CSV_PATH, SUBJECTS_TO_FETCH, DATA_DIR
from transformation.cleaner import clean_book_record
from storage.db import init_db, insert_books

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Intermediate data paths
TEMP_DIR = os.path.join(DATA_DIR, "temp")
INGESTED_FILE = os.path.join(TEMP_DIR, "ingested.json")
TRANSFORMED_FILE = os.path.join(TEMP_DIR, "transformed.json")

def ensure_temp_dir():
    os.makedirs(TEMP_DIR, exist_ok=True)

def save_temp_data(data: List[Dict[str, Any]], filepath: str):
    ensure_temp_dir()
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved {len(data)} records to {filepath}")

def load_temp_data(filepath: str) -> List[Dict[str, Any]]:
    if not os.path.exists(filepath):
        logger.warning(f"File {filepath} not found.")
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

# ANSI Color Codes
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def log_step(message):
    logger.info(f"{BOLD}{CYAN}>>> {message}{RESET}")

def run_ingestion(limit: int = 20):
    log_step("Starting Ingestion Phase...")
    
    # 1. Load from CSV
    logger.info(f"Loading from CSV: {DEFAULT_CSV_PATH}")
    csv_books = load_csv(DEFAULT_CSV_PATH)
    
    # 2. Load from API
    logger.info(f"Loading from OpenLibrary API for subjects: {SUBJECTS_TO_FETCH} with limit={limit}")
    api_books = load_all_openlibrary_data(SUBJECTS_TO_FETCH, limit=limit)
    
    all_books = csv_books + api_books
    logger.info(f"{GREEN}Ingestion complete. Total records: {len(all_books)}{RESET}")
    
    save_temp_data(all_books, INGESTED_FILE)

def run_transformation():
    log_step("Starting Transformation Phase...")
    
    raw_books = load_temp_data(INGESTED_FILE)
    if not raw_books:
        logger.warning(f"{YELLOW}No data to transform.{RESET}")
        return

    # Deduplication Logic
    cleaned_books = []
    seen = set() # Store tuples of (title_lower, author_lower)

    for book in raw_books:
        clean_book = clean_book_record(book)
        
        # Create a unique key
        t = (clean_book.get('title') or "").lower()
        a = (clean_book.get('author') or "").lower()
        key = (t, a)
        
        if key not in seen and t: # Ensure title exists
            seen.add(key)
            cleaned_books.append(clean_book)
        
    logger.info(f"{GREEN}Transformation complete. Processed {len(cleaned_books)} unique records (dropped {len(raw_books) - len(cleaned_books)} duplicates).{RESET}")
    save_temp_data(cleaned_books, TRANSFORMED_FILE)

def run_storage():
    log_step("Starting Storage Phase...")
    
    books_to_store = load_temp_data(TRANSFORMED_FILE)
    if not books_to_store:
        logger.warning(f"{YELLOW}No data to store.{RESET}")
        return

    # Initialize DB (idempotent)
    init_db()
    
    # Insert
    insert_books(books_to_store)
    logger.info(f"{GREEN}Storage Phase complete.{RESET}")

from transformation.embedder import load_model, generate_embeddings, save_embeddings
from storage.db import get_recent_books

def run_embedding():
    log_step("Starting Embedding Phase...")
    
    # Fetch all books from DB to embed
    # Using a large limit to get all (for this scale)
    books = get_recent_books(limit=100000)
    if not books:
        logger.warning(f"{YELLOW}No books found in DB to embed.{RESET}")
        return

    model = load_model()
    data = generate_embeddings(books, model)
    
    save_embeddings(data)
    logger.info(f"{GREEN}Embedding Phase complete.{RESET}")

def run_all(limit: int = 20):
    run_ingestion(limit=limit)
    run_transformation()
    run_storage()
    run_embedding()
    logger.info(f"{BOLD}{GREEN}Full Pipeline Run Complete 🚀{RESET}")

def main():
    parser = argparse.ArgumentParser(description="Book Finder Data Pipeline")
    parser.add_argument("--ingest", action="store_true", help="Run Ingestion Phase")
    parser.add_argument("--transform", action="store_true", help="Run Transformation Phase")
    parser.add_argument("--store", action="store_true", help="Run Storage Phase")
    parser.add_argument("--embed", action="store_true", help="Run Embedding Phase (New)")
    parser.add_argument("--all", action="store_true", help="Run All Phases")
    parser.add_argument("--limit", type=int, default=20, help="Limit number of books per subject from API")
    parser.add_argument("--target", type=int, dest='limit', help="Alias for --limit") # Support user's target arg
    
    args = parser.parse_args()
    
    if args.all:
        run_all(limit=args.limit)
    else:
        if args.ingest:
            run_ingestion(limit=args.limit)
        if args.transform:
            run_transformation()
        if args.store:
            run_storage()
        if args.embed:
            run_embedding()
            
    if not (args.ingest or args.transform or args.store or args.embed or args.all):
        parser.print_help()

if __name__ == "__main__":
    main()
