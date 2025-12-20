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
        SELECT b.id, b.published_date, b.title, b.author, c.name AS category_name
        FROM books b
        LEFT JOIN categories c ON b.category_id = c.id
        ORDER BY b.id DESC
    """
    books = conn.execute(query).fetchall()
    conn.close()
    return books
