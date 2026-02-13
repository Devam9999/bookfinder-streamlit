# ingestion/csv_loader.py
import pandas as pd
import logging
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def normalize_csv_record(row: Dict[str, Any]) -> Dict[str, Optional[str]]:
    """
    Normalizes a CSV row into the standard input format.
    Handles column name variations.
    """
    # Define possible column names for each field
    title_cols = ['Title', 'title', 'book_name', 'Name']
    desc_cols = ['Description', 'description', 'summary', 'about', 'Plot']
    genre_cols = ['Genre', 'genre', 'subjects', 'category']
    isbn_cols = ['ISBN', 'isbn', 'Isbn']
    author_cols = ['Author', 'author', 'Writer', 'writer']
    cover_image_cols = ['Cover_Image', 'cover_image', 'Image', 'image']
    publish_year_cols = ['Publish_Year', 'publish_year', 'Year', 'year']

    title = None
    description = None
    genre = None
    isbn = None
    author = None
    cover_image = None
    publish_year = None

    # Helper to find first matching column
    def transform_field(cols, row):
        for col in cols:
            if col in row and pd.notna(row[col]):
                return str(row[col]).strip()
        return None

    title = transform_field(title_cols, row)
    description = transform_field(desc_cols, row)
    genre = transform_field(genre_cols, row)
    isbn = transform_field(isbn_cols, row)
    author = transform_field(author_cols, row)
    cover_image = transform_field(cover_image_cols, row)
    publish_year = transform_field(publish_year_cols, row)

    return {
        "isbn": isbn,
        "title": title,
        "description": description,
        "author": author,
        "genre": genre,
        "cover_image": cover_image,
        "publish_year": publish_year,
        "source": "csv"
    }

def load_csv(file_path: str) -> List[Dict[str, Optional[str]]]:
    """
    Loads books from a CSV file.
    Returns a list of authorized book dictionaries.
    """
    if not file_path.endswith('.csv'):
        logger.error(f"File {file_path} is not a CSV file.")
        return []

    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully loaded CSV from {file_path} with {len(df)} rows.")
        
        books = []
        for _, row in df.iterrows():
            clean_record = normalize_csv_record(row.to_dict())
            books.append(clean_record)
            
        return books
    
    except FileNotFoundError:
        logger.error(f"CSV file not found at {file_path}")
        return []
    except Exception as e:
        logger.error(f"Error loading CSV {file_path}: {e}")
        return []
