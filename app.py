from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps
from passlib.hash import django_pbkdf2_sha256
from apps.categories.routes import categories_bp
from apps.books.routes import books_bp

# -----------------------------
# Create Flask app and load config
# -----------------------------
app = Flask(__name__)
app.config.from_object("config.Config")
app.secret_key = app.config["SECRET_KEY"]  # needed for session

# -----------------------------
# Database connection helper
# -----------------------------
def get_db_connection():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# Login required decorator
# -----------------------------
def login_required(f):
    """Decorator to protect routes that require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# -----------------------------
# Login route
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login and session setup."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Connect to DB
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM auth_user WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        # Verify password using Django hash
        if user and django_pbkdf2_sha256.verify(password, user["password"]):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            # Redirect to books list (change to preferred module)
            return redirect(url_for("books.list"))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

# -----------------------------
# Logout route
# -----------------------------
@app.route("/logout")
def logout():
    """Clear session and redirect to login."""
    session.clear()
    return redirect(url_for("login"))

# -----------------------------
# Register Blueprints
# -----------------------------
app.register_blueprint(categories_bp, url_prefix="/categories")
app.register_blueprint(books_bp, url_prefix="/books")

# -----------------------------
# Global login protection
# -----------------------------
@app.before_request
def require_login():
    """Redirect to login if not logged in (skip login page and static files)."""
    if request.endpoint not in ("login", "static", "page_not_found"):
        if "user_id" not in session:
            return redirect(url_for("login"))

# -----------------------------
# 404 error handler
# -----------------------------
@app.errorhandler(404)
def page_not_found(e):
    """Render the global 404 page."""
    return render_template("404.html"), 404

# -----------------------------
# Main entry
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
