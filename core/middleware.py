"""
core/middleware.py

Global request middleware for the Flask project.

This file defines `register_middleware()` which attaches application-wide
before_request hooks. Currently, it enforces login for protected routes.
"""

from flask import request, redirect, url_for, session


# -----------------------------
# Register Middleware
# -----------------------------
def register_middleware(app):
    """
    Attach global before_request hooks to the Flask app.

    Currently enforces that users must be logged in to access protected routes.
    """

    @app.before_request
    def require_login():
        """
        Redirect unauthenticated users to the login page.

        Rules:
            - Skip login requirement for the following endpoints:
                * login
                * static (for CSS, JS, images)
                * page_not_found (404 handler)
            - If 'user_id' not in session, redirect to '/login'
        """
        if request.endpoint in ("login", "static", "page_not_found"):
            # Allow unauthenticated access to these endpoints
            return

        # Require login for all other routes
        if "user_id" not in session:
            return redirect(url_for("login"))
