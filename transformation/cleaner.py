# transformation/cleaner.py
import re
import html
import logging
from typing import Dict, Any, Optional

# Configure logging
logger = logging.getLogger(__name__)

def clean_text(text: Optional[str]) -> Optional[str]:
    """
    Cleans a text string:
    - Decodes HTML entities
    - Removes HTML tags
    - Normalizes whitespace
    - Converts empty or placeholder strings to None
    """
    if text is None:
        return None
    
    if not isinstance(text, str):
        text = str(text)

    # Decode HTML entities
    text = html.unescape(text)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Normalize whitespace (replace multiple spaces/newlines with single space)
    text = re.sub(r'\s+', ' ', text).strip()

    # Check for placeholder values
    placeholders = {"description not available", "no description", "n/a", "", "none", "null"}
    if text.lower() in placeholders:
        return None
        
    return text

def clean_book_record(book: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cleans a book record dictionary.
    """
    cleaned_book = book.copy()
    
    cleaned_book['title'] = clean_text(cleaned_book.get('title'))
    cleaned_book['description'] = clean_text(cleaned_book.get('description'))
    cleaned_book['genre'] = clean_text(cleaned_book.get('genre'))
    cleaned_book['isbn'] = clean_text(cleaned_book.get('isbn'))
    cleaned_book['author'] = clean_text(cleaned_book.get('author'))
    
    # Simple year cleaning (keep only digits if possible, or just text clean)
    pub_year = cleaned_book.get('publish_year')
    if pub_year:
        pub_year = clean_text(str(pub_year))
        # Optional: Extract just the year if it's a date "2020-01-01" -> "2020"
        # For now, just basic text clean
    cleaned_book['publish_year'] = pub_year
    
    # Cover image usually needs no cleaning if it's a URL, but check for None
    cleaned_book['cover_image'] = cleaned_book.get('cover_image')

    # Source is internal metadata
    if cleaned_book.get('source'):
        cleaned_book['source'] = str(cleaned_book['source']).strip()
        
    return cleaned_book
