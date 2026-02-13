# storage/db.py
import sqlite3
import os
import logging
from typing import List, Dict, Any, Optional
from ingestion.config import DB_PATH







def normalize(text: Optional[str]) -> str:
    """
    Standardizes text for consistent deduplication.
    - Lowercases
    - Strips leading/trailing spaces
    - Removes extra internal spaces
    """
    if not text:
        return ""
    return " ".join(text.strip().lower().split())










# Configure logging
logger = logging.getLogger(__name__)

# Schema path
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row # Access columns by name
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection failed: {e}")
        return None

def init_db():
    """
    Initializes the database with the schema.
    """
    logger.info("Initializing database...")
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = get_db_connection()
    if not conn:
        return

    try:
        with open(SCHEMA_PATH, 'r') as f:
            schema = f.read()
        
        cursor = conn.cursor()
        cursor.executescript(schema)
        conn.commit()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
    finally:
        conn.close()



def insert_books(books: List[Dict[str, Any]]):
    """
    Bulk inserts valid books into the database.
    Uses INSERT OR IGNORE to skip duplicates based on UNIQUE(title, author).
    Applies strong normalization before deduplication and insertion.
    """
    if not books:
        logger.info("No books to insert.")
        return

    # In-memory deduplication using normalized values
    seen = set()
    deduplicated_books = []
    skipped_in_memory = 0

    for book in books:
        normalized_title = normalize(book.get('title'))
        normalized_author = normalize(book.get('author'))

        if not normalized_title:
            skipped_in_memory += 1
            continue

        key = (normalized_title, normalized_author)

        if key not in seen:
            seen.add(key)
            # Store normalized values back into book copy
            book_copy = book.copy()
            book_copy['title'] = normalized_title
            book_copy['author'] = normalized_author
            book_copy['isbn'] = normalize(book.get('isbn'))
            deduplicated_books.append(book_copy)
        else:
            skipped_in_memory += 1

    if skipped_in_memory > 0:
        logger.info(f"Skipped {skipped_in_memory} duplicate(s) in memory before insertion.")

    if not deduplicated_books:
        logger.info("No unique books to insert after deduplication.")
        return

    conn = get_db_connection()
    if not conn:
        return

    query = """
    INSERT OR IGNORE INTO books 
    (isbn, title, description, author, genre, cover_image, publish_year, source)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    data_to_insert = [
        (
            book.get('isbn'),
            book.get('title'),
            book.get('description'),
            book.get('author'),
            book.get('genre'),
            book.get('cover_image'),
            book.get('publish_year'),
            book.get('source')
        )
        for book in deduplicated_books
    ]

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM books")
        count_before = cursor.fetchone()[0]

        cursor.executemany(query, data_to_insert)
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM books")
        count_after = cursor.fetchone()[0]

        inserted = count_after - count_before
        skipped_db = len(data_to_insert) - inserted

        logger.info(f"Successfully inserted {inserted} new book(s).")
        if skipped_db > 0:
            logger.info(f"Skipped {skipped_db} duplicate(s) already in database.")

    except sqlite3.Error as e:
        logger.error(f"Error inserting books: {e}")
    finally:
        conn.close()



# def insert_books(books: List[Dict[str, Any]]):
#     """
#     Bulk inserts valid books into the database.
#     Uses INSERT OR IGNORE to skip duplicates based on UNIQUE(title, author) constraint.
#     Also performs in-memory deduplication before insertion.
#     """
#     if not books:
#         logger.info("No books to insert.")
#         return

#     # In-memory deduplication: keep only unique (title, author) pairs
#     seen = set()
#     deduplicated_books = []
#     skipped_in_memory = 0
    
#     for book in books:
#         title = (book.get('title') or '').strip()
#         author = (book.get('author') or '').strip()
        
#         # Skip if title is empty
#         if not title:
#             skipped_in_memory += 1
#             continue
        
#         # Create normalized key (case-insensitive)
#         key = (title.lower(), author.lower())
        
#         if key not in seen:
#             seen.add(key)
#             deduplicated_books.append(book)
#         else:
#             skipped_in_memory += 1
    
#     if skipped_in_memory > 0:
#         logger.info(f"Skipped {skipped_in_memory} duplicate(s) in memory before insertion.")
    
#     if not deduplicated_books:
#         logger.info("No unique books to insert after deduplication.")
#         return

#     conn = get_db_connection()
#     if not conn:
#         return
    
#     # Use INSERT OR IGNORE to skip duplicates at database level
#     query = """
#     INSERT OR IGNORE INTO books (isbn, title, description, author, genre, cover_image, publish_year, source)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#     """
    
#     # Prepare data for insertion (list of tuples)
#     data_to_insert = []
#     for book in deduplicated_books:
#         data_to_insert.append((
#             book.get('isbn'),
#             book.get('title'),
#             book.get('description'),
#             book.get('author'),
#             book.get('genre'),
#             book.get('cover_image'),
#             book.get('publish_year'),
#             book.get('source')
#         ))
    
#     try:
#         cursor = conn.cursor()
        
#         # Get count before insertion
#         cursor.execute("SELECT COUNT(*) FROM books")
#         count_before = cursor.fetchone()[0]
        
#         # Insert with OR IGNORE
#         cursor.executemany(query, data_to_insert)
#         conn.commit()
        
#         # Get count after insertion
#         cursor.execute("SELECT COUNT(*) FROM books")
#         count_after = cursor.fetchone()[0]
        
#         inserted = count_after - count_before
#         skipped_db = len(data_to_insert) - inserted
        
#         logger.info(f"Successfully inserted {inserted} new book(s).")
#         if skipped_db > 0:
#             logger.info(f"Skipped {skipped_db} duplicate(s) already in database.")
#     except sqlite3.Error as e:
#         logger.error(f"Error inserting books: {e}")
#     finally:
#         conn.close()

def get_recent_books(limit: int = 100) -> List[Dict[str, Any]]:
    """
    Fetches the most recent books from the database.
    """
    conn = get_db_connection()
    if not conn:
        return []

    query = """
    SELECT id, isbn, title, description, author, genre, cover_image, publish_year, source, created_at 
    FROM books 
    ORDER BY created_at DESC 
    LIMIT ?
    """
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error fetching books: {e}")
        return []
    finally:
        conn.close()

def search_books(query_text: str, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Searches books by title, author, description, or genre.
    """
    conn = get_db_connection()
    if not conn:
        return []

    sql = """
    SELECT id, isbn, title, description, author, genre, cover_image, publish_year, source, created_at 
    FROM books 
    WHERE title LIKE ? 
       OR description LIKE ? 
       OR author LIKE ?
       OR genre LIKE ?
    ORDER BY created_at DESC 
    LIMIT ?
    """
    search_term = f"%{query_text}%"
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (search_term, search_term, search_term, search_term, limit))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error searching books: {e}")
        return []
    finally:
        conn.close()

def get_books_by_ids(ids: List[int]) -> List[Dict[str, Any]]:
    """
    Fetches books by a list of IDs.
    """
    if not ids:
        return []
    
    conn = get_db_connection()
    if not conn:
        return []
    
    placeholders = ', '.join('?' for _ in ids)
    sql = f"""
    SELECT id, isbn, title, description, author, genre, cover_image, publish_year, source, created_at 
    FROM books 
    WHERE id IN ({placeholders})
    """
    
    # Preserve order of IDs if possible, but SQL IN doesn't guarantee it.
    # Application layer can re-sort.
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql, tuple(ids))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error fetching books by IDs: {e}")
        return []
    finally:
        conn.close()

def get_database_stats() -> Dict[str, int]:
    """
    Returns statistics about the database: total books, authors, and genres.
    """
    conn = get_db_connection()
    if not conn:
        return {"total_books": 0, "total_authors": 0, "total_genres": 0}
    
    stats = {}
    
    try:
        cursor = conn.cursor()
        
        # Total Books
        cursor.execute("SELECT COUNT(*) FROM books")
        stats["total_books"] = cursor.fetchone()[0]
        
        # Total Authors
        cursor.execute("SELECT COUNT(DISTINCT author) FROM books")
        stats["total_authors"] = cursor.fetchone()[0]
        
        # Total Genres (approximate as genres are comma separated strings sometimes)
        cursor.execute("SELECT COUNT(DISTINCT genre) FROM books")
        stats["total_genres"] = cursor.fetchone()[0]
        
    except sqlite3.Error as e:
        logger.error(f"Error fetching database stats: {e}")
        return {"total_books": 0, "total_authors": 0, "total_genres": 0}
    finally:
        conn.close()
    
    return stats

def get_book_ids_by_genres(genres: List[str]) -> List[int]:
    """
    Fetches IDs of books that match any of the provided genres (case-insensitive partial match).
    """
    if not genres:
        return []

    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        
        # Construct query dynamically for multiple genres
        conditions = []
        params = []
        for genre in genres:
            conditions.append("genre LIKE ?")
            params.append(f"%{genre}%")
            
        where_clause = " OR ".join(conditions)
        query = f"SELECT id FROM books WHERE {where_clause}"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error fetching IDs by genres: {e}")
        return []
    finally:
        conn.close()
