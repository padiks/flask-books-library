"""
core/app_factory.py

Application factory for the Flask project.

This file defines `create_app()`, which builds and configures the Flask app.
It handles:
    - Template and static folder paths
    - Loading configuration
    - Root route redirection (login or books list)
    - Blueprint registration
    - Global authentication, error handlers, and middleware
"""

import os
from flask import Flask, redirect, url_for, session

from config import Config

# Import blueprints (feature-based modules)
from apps.primer.routes import primer_bp
from apps.categories.routes import categories_bp
from apps.books.routes import books_bp
from apps.excel.routes import excel_bp

# Import core infrastructure
from core.auth import register_auth
from core.errors import register_error_handlers
from core.middleware import register_middleware


# -----------------------------
# Project root directory
# -----------------------------
# BASE_DIR points to the top-level project folder
BASE_DIR = os.path.abspath(
    os.path.dirname(os.path.dirname(__file__))
)
# └── project_folder/


# -----------------------------
# Application Factory
# -----------------------------
def create_app():
    """Builds and returns a fully configured Flask application."""

    # Create Flask app with explicit template and static paths
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static"),
    )

    # Load configuration from config.py
    app.config.from_object(Config)

    # -------------------------
    # Root route
    # -------------------------
    # Redirects users to the appropriate page:
    # - If logged in, go to books list
    # - Otherwise, go to login page
    @app.route("/")
    def index():
        if "user_id" in session:
            return redirect(url_for("books.list"))
        return redirect(url_for("login"))

    # -------------------------
    # Register blueprints
    # -------------------------
    # Modular feature-based routes (e.g., books, categories)
    app.register_blueprint(primer_bp, url_prefix="/primer")		
    app.register_blueprint(categories_bp, url_prefix="/categories")
    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(excel_bp, url_prefix="/excel")		

    # -------------------------
    # Register global infrastructure
    # -------------------------
    # Authentication, error handlers, and middleware
    register_auth(app)
    register_error_handlers(app)
    register_middleware(app)

    # Return the configured Flask app
    return app
