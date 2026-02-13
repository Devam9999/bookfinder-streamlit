# serving/api.py
import sys
import os
import warnings
import logging

# Suppress non-critical warnings for cleaner startup
warnings.filterwarnings('ignore', category=FutureWarning)
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
logging.getLogger("transformers").setLevel(logging.ERROR)

# Add the parent directory to sys.path to resolve 'storage' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from storage.db import get_recent_books, get_books_by_ids
from transformation.embedder import load_model, load_embeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# --- METADATA ---
tags_metadata = [
    {"name": "Books", "description": "Operations with books (retrieval, listing)."},
    {"name": "Search", "description": "Semantic search capabilities."},
    {"name": "System", "description": "Health checks and status."},
]

app = FastAPI(
    title="Book Finder API",
    description="Product-grade API for semantic book search and retrieval. Built with FastAPI and Sentence Transformers.",
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "Data Engineering Team",
        "email": "support@bookfinder.com",
    },
)

# --- MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---
class Book(BaseModel):
    id: int = Field(..., description="Unique database identifier")
    isbn: Optional[str] = Field(None, description="ISBN-13 or ISBN-10")
    title: Optional[str] = Field(None, description="Book title")
    description: Optional[str] = Field(None, description="Book abstract or summary")
    author: Optional[str] = Field(None, description="Primary author")
    genre: Optional[str] = Field(None, description="Genre or subject")
    cover_image: Optional[str] = Field(None, description="URL to cover image")
    publish_year: Optional[str] = Field(None, description="Year of publication")
    source: Optional[str] = Field(None, description="Data source (e.g. OpenLibrary)")
    created_at: Optional[str] = Field(None, description="Record creation timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 101,
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "genre": "Classic",
                "publish_year": "1925"
            }
        }

class SearchResponse(BaseModel):
    query: str
    results: List[Book]
    count: int

# --- RESOURCES ---
# Load ML models on startup (or lazy load)
# Note: In a real production app, use Lifespan events
model = None
embeddings_data = None

@app.on_event("startup")
def load_resources():
    global model, embeddings_data
    try:
        model = load_model()
        embeddings_data = load_embeddings()
        print("✅ ML Resources Loaded")
    except Exception as e:
        print(f"⚠️ Warning: utilizing fallback (No ML): {e}")

# --- ENDPOINTS ---

@app.get("/", tags=["System"])
def health_check():
    """
    **Health Check**
    
    Returns the operational status of the API and loaded models.
    """
    ml_status = "active" if (model and embeddings_data) else "inactive"
    return {
        "status": "online", 
        "version": "1.0.0",
        "ml_engine": ml_status,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/books/recent", response_model=List[Book], tags=["Books"])
def get_recent_books_endpoint(limit: int = Query(10, ge=1, le=100, description="Number of books to return (1-100)")):
    """
    **Get Recent Books**
    
    Returns the most recently indexed books from the library.
    """
    try:
        books = get_recent_books(limit)
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search", response_model=SearchResponse, tags=["Search"])
def semantic_search_endpoint(
    q: str = Query(..., min_length=3, description="Natural language search query"),
    limit: int = Query(10, ge=1, le=50)
):
    """
    **Semantic Search**
    
    Performs a vector-based semantic search to find books matching the *meaning* of the query.
    
    - **q**: Your search query (e.g., "apocalyptic robot futures")
    - **limit**: Max results to return
    """
    if not model or not embeddings_data:
        raise HTTPException(status_code=503, detail="Search engine not ready (embeddings missing)")
        
    try:
        # Encode and Search
        query_vec = model.encode([q])
        stored_vecs = embeddings_data['embeddings']
        
        scores = cosine_similarity(query_vec, stored_vecs)[0]
        top_indices = np.argsort(scores)[::-1][:limit * 3] # Fetch 3x for dedup
        
        ids = np.array(embeddings_data['ids'])[top_indices]
        scores = scores[top_indices]
        
        books = get_books_by_ids(ids.tolist())
        
        # Hydrate and Order
        book_map = {b['id']: b for b in books}
        ordered_books = []
        seen = set()
        
        for bid, score in zip(ids, scores):
            if len(ordered_books) >= limit: break
            
            book = book_map.get(bid)
            if not book: continue
            
            # Simple Dedup by Title+Author
            key = (book.get('title', '').lower(), book.get('author', '').lower())
            if key in seen: continue
            seen.add(key)
            
            ordered_books.append(book)
            
        return {
            "query": q,
            "results": ordered_books,
            "count": len(ordered_books)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
