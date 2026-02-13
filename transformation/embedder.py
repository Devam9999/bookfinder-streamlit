# transformation/embedder.py
import pickle
import os
import logging
import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from ingestion.config import DATA_DIR

# Configure logging
logger = logging.getLogger(__name__)

EMBEDDINGS_FILE = os.path.join(DATA_DIR, "embeddings.pkl")
# Use a small, fast model suitable for local pipelines
MODEL_NAME = 'all-MiniLM-L6-v2'

def load_model():
    """
    Loads the sentence transformer model.
    """
    logger.info(f"Loading embedding model: {MODEL_NAME}...")
    return SentenceTransformer(MODEL_NAME)

def generate_text_for_embedding(book: Dict[str, Any]) -> str:
    """
    Combines fields to create a rich text representation for embedding.
    """
    title = book.get('title') or ""
    description = book.get('description') or ""
    genre = book.get('genre') or ""
    author = book.get('author') or ""
    
    # Structured combination: Clearer signals for the model
    return f"Title: {title}. Author: {author}. Genres: {genre}. Description: {description}."

def generate_embeddings(books: List[Dict[str, Any]], model) -> Dict[str, Any]:
    """
    Generates embeddings for a list of books.
    Returns a dictionary containing IDs and the embedding matrix.
    """
    if not books:
        return {}

    logger.info(f"Generating embeddings for {len(books)} books...")
    
    texts = [generate_text_for_embedding(b) for b in books]
    # Normalize embeddings for cosine similarity via dot product
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    
    # Store ID mapping to link back to DB
    ids = [book['id'] for book in books]
    
    return {
        "ids": ids,
        "embeddings": embeddings
    }

def save_embeddings(data: Dict[str, Any]):
    """
    Saves embeddings to a pickle file.
    """
    with open(EMBEDDINGS_FILE, 'wb') as f:
        pickle.dump(data, f)
    logger.info(f"Embeddings saved to {EMBEDDINGS_FILE}")

def load_embeddings() -> Dict[str, Any]:
    """
    Loads embeddings from the pickle file.
    """
    if not os.path.exists(EMBEDDINGS_FILE):
        logger.warning(f"Embeddings file {EMBEDDINGS_FILE} not found.")
        return {}
        
    with open(EMBEDDINGS_FILE, 'rb') as f:
        return pickle.load(f)
