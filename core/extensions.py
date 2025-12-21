"""
core/extensions.py

Shared extensions and helpers for the Flask project.

This file centralizes utilities like database connections, so blueprints
and other modules can reuse them consistently.
"""

import sqlite3
from flask import current_app


# -----------------------------
# Database Connection Helper
# -----------------------------
def get_db_connection():
    """
    Create and return a SQLite database connection using the app's configuration.

    Features:
        - Uses `current_app.config["DATABASE"]` to locate the DB file
        - Sets `row_factory` to `sqlite3.Row` for dict-like access to rows

    Returns:
        sqlite3.Connection: A connection object to the SQLite database
    """
    conn = sqlite3.connect(current_app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn
