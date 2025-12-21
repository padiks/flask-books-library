import sqlite3
from flask import current_app

def get_db_connection():
    db_path = current_app.config["DATABASE"]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_books():
    """Return all books with category name."""
    conn = get_db_connection()
    query = """
        SELECT b.*, c.name AS category_name
        FROM books b
        LEFT JOIN categories c ON b.category_id = c.id
        ORDER BY b.id DESC
    """
    books = conn.execute(query).fetchall()
    conn.close()
    return books


def get_book(id):
    """Return a single book with category name."""
    conn = get_db_connection()
    query = """
        SELECT b.*, c.name AS category_name
        FROM books b
        LEFT JOIN categories c ON b.category_id = c.id
        WHERE b.id = ?
    """
    book = conn.execute(query, (id,)).fetchone()
    conn.close()
    return book


def get_categories():
    """Return all categories for dropdowns."""
    conn = get_db_connection()
    categories = conn.execute(
        "SELECT id, name FROM categories ORDER BY name"
    ).fetchall()
    conn.close()
    return categories
