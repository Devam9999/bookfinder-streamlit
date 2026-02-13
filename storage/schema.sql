CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn TEXT ,
    title TEXT NOT NULL,
    description TEXT,
    author TEXT,
    genre TEXT,
    cover_image TEXT,
    publish_year TEXT,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(title, author) ON CONFLICT IGNORE
);
