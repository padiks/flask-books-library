"""
app.py

Entry point for the Flask application.

This file is minimal because the application logic has been modularized
into the 'core' and 'apps' folders. It simply creates the Flask app using
the application factory pattern and runs it.

Structure:
    - core/app_factory.py -> create_app(): builds and configures the Flask app
    - apps/               -> feature-based blueprints (books, categories, etc.)
    - templates/          -> project-wide templates (base.html, 404.html, etc.)
    - static/             -> CSS, JS, images
    - instance/           -> SQLite database (db.sqlite3)
"""

# Import the application factory from core
from core.app_factory import create_app

# -----------------------------
# Create the Flask app
# -----------------------------
# create_app() returns a fully configured Flask app with:
# - registered blueprints (modules like books, categories)
# - global error handlers (404, 500)
# - authentication and middleware
app = create_app()

# -----------------------------
# Main entry point
# -----------------------------
# Run the app if this file is executed directly.
# 'debug=True' enables hot reload and better error messages in development.
if __name__ == "__main__":
    app.run(debug=True)
