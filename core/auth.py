"""
core/auth.py

Authentication routes and session management for the Flask project.

This file registers login and logout routes using the `register_auth()` function.
It keeps authentication logic centralized, so blueprints do not handle sessions directly.
"""

from flask import render_template, request, redirect, url_for, session, flash
from passlib.hash import django_pbkdf2_sha256

from core.extensions import get_db_connection  # Shared DB connection helper


# -----------------------------
# Register Authentication Routes
# -----------------------------
def register_auth(app):
    """
    Attach login and logout routes to the Flask app.

    Routes:
        - /login  : Handles user login and session setup
        - /logout : Clears session and redirects to login
    """

    # -------------------------
    # Login Route
    # -------------------------
    @app.route("/login", methods=["GET", "POST"])
    def login():
        """
        Handle user login.

        POST:
            - Verifies username and password against the database
            - Sets session['user_id'] and session['username'] on success
            - Redirects to books list if login succeeds
        GET:
            - Renders the login form template
        """

        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            # Connect to DB and fetch user
            conn = get_db_connection()
            user = conn.execute(
                "SELECT * FROM auth_user WHERE username = ?",
                (username,)
            ).fetchone()
            conn.close()

            # Verify password using Django PBKDF2 hash
            if user and django_pbkdf2_sha256.verify(password, user["password"]):
                # Successful login
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                return redirect(url_for("books.list"))

            # Invalid credentials
            flash("Invalid username or password", "error")
            return redirect(url_for("login"))

        # GET request: show login form
        return render_template("login.html")

    # -------------------------
    # Logout Route
    # -------------------------
    @app.route("/logout")
    def logout():
        """
        Clear user session and redirect to login page.
        """
        session.clear()
        return redirect(url_for("login"))
