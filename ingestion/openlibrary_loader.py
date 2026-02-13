# ingestion/openlibrary_loader.py
import requests
import logging
import time
from typing import List, Dict, Optional
from ingestion.config import OPENLIBRARY_SEARCH_URL

# Configure logging
logger = logging.getLogger(__name__)

def fetch_books_from_openlibrary(subject: str, limit: int = 20) -> List[Dict[str, Optional[str]]]:
    """
    Fetches books from OpenLibrary API by subject.
    Normalizes them to the standard format.
    """
    logger.info(f"Fetching books for subject: {subject}...")
    
    params = {
        "subject": subject,
        "limit": limit,
        "fields": "title,first_sentence,subject,cover_i,author_name,key,isbn,publish_year" 
        # Note: 'description' often requires a separate call per book in OpenLibrary, 
        # but 'first_sentence' or using search API returns some blurb. 
        # For simplicity in this pipeline, we will use 'first_sentence' as a proxy for description
        # or handle missing descriptions gracefully as per requirements.
    }
    
    try:
        response = requests.get(OPENLIBRARY_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        docs = data.get("docs", [])
        logger.info(f"Found {len(docs)} books for subject {subject}.")
        
        books = []
        for doc in docs:
            # OpenLibrary search results structure is messy.
            # 'first_sentence' is a list or string.
            description = None
            if "first_sentence" in doc:
                val = doc["first_sentence"]
                if isinstance(val, list) and val:
                    description = val[0]
                elif isinstance(val, str):
                    description = val
            
            # Extract genre (subject)
            genre = subject
            if "subject" in doc and doc["subject"]:
                # Just take the first few as a string
                genre = ", ".join(doc["subject"][:3])

            # Extract newly requested fields
            isbn_list = doc.get('isbn', [])
            isbn = isbn_list[0] if isbn_list else None
            
            author_list = doc.get('author_name', [])
            author = author_list[0] if author_list else None
            
            publish_year_list = doc.get('publish_year', [])
            publish_year = str(publish_year_list[0]) if publish_year_list else None
            
            cover_i = doc.get('cover_i')
            cover_image = f"https://covers.openlibrary.org/b/id/{cover_i}-L.jpg" if cover_i else None

            book = {
                "isbn": isbn,
                "title": doc.get("title"),
                "description": description,
                "author": author,
                "genre": genre,
                "cover_image": cover_image,
                "publish_year": publish_year,
                "source": "openlibrary"
            }
            # Mandatory: Missing values must be None
            # The dictionary.get() method defaults to None if key missing, which is good.
            # Ensuring explicit None for empty strings if any
            for k, v in book.items():
                if v == "":
                    book[k] = None
            
            books.append(book)
            
        return books

    except requests.RequestException as e:
        logger.error(f"Error fetching data from OpenLibrary for subject {subject}: {e}")
        return []

def load_all_openlibrary_data(subjects: List[str], limit: int = 20) -> List[Dict[str, Optional[str]]]:
    """
    Aggregates data from multiple subjects.
    """
    all_books = []
    for subject in subjects:
        books = fetch_books_from_openlibrary(subject, limit=limit)
        all_books.extend(books)
        time.sleep(1) # Be nice to the API
    
    return all_books
