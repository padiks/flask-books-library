"""
core/errors.py

Global error handlers for the Flask project.

This file defines `register_error_handlers()` which attaches application-wide
error handlers, keeping blueprints free of repetitive error logic.
"""

from flask import render_template


# -----------------------------
# Register Global Error Handlers
# -----------------------------
def register_error_handlers(app):
    """
    Attach global error handlers to the Flask app.

    Currently handles:
        - 404 Not Found
        (Additional handlers like 500, 403 can be added here)
    """

    @app.errorhandler(404)
    def page_not_found(e):
        """
        Render the global 404 page when a resource is not found.

        Args:
            e: The exception object (not used here)

        Returns:
            Rendered 404 template with HTTP status code 404
        """
        return render_template("404.html"), 404
