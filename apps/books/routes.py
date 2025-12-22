import sqlite3
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session, abort
from .models import get_all_books, get_book, get_categories
from core.extensions import get_db_connection  # DB connection helper coming from core/extensions.py

books_bp = Blueprint(
    "books",
    __name__,
    template_folder="templates"
)

# ---------------------------
# Admin Required Decorator
# ---------------------------
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") != "admin":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------
# List Books
# ---------------------------
@books_bp.route("/")
def list():
    books = get_all_books()
    return render_template("books/list.html", items=books)

# ---------------------------
# List Books
# ---------------------------
#@books_bp.route("/")
#def list():
#    books = get_all_books()
    # Sort books by published_date from latest to oldest
#    books_sorted = sorted(books, key=lambda b: b['published_date'], reverse=True)
#    return render_template("books/list.html", items=books_sorted)	
		
# ---------------------------
# View Book
# ---------------------------
@books_bp.route("/view/<int:id>")
def view(id):
    book = get_book(id)

    if book is None:
        flash("Book not found.", "error")
        return redirect(url_for("books.list"))

    return render_template("books/view.html", book=book, title="Book Details")

# ---------------------------
# Add Book (Admin Only)
# ---------------------------
@books_bp.route("/add", methods=["GET", "POST"])
@admin_required
def add():
    categories = get_categories()

    if request.method == "POST":
        published_date = request.form.get("published_date")
        title = request.form.get("title", "").strip()
        hepburn = request.form.get("hepburn", "").strip()
        author = request.form.get("author", "").strip()
        release = request.form.get("release", "").strip()
        url = request.form.get("url", "").strip()
        summary = request.form.get("summary", "").strip()
        category_id = request.form.get("category_id")

        # Minimal validation
        if not title or not hepburn or not author or not release or not url:
            flash("All required fields must be filled.", "error")
        else:
            db_path = current_app.config["DATABASE"]

            with sqlite3.connect(db_path, timeout=5) as conn:
                conn.execute(
                    """
                    INSERT INTO books (
                        published_date,
                        title,
                        hepburn,
                        author,
                        release,
                        url,
                        summary,
                        category_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        published_date,
                        title,
                        hepburn,
                        author,
                        release,
                        url,
                        summary,
                        category_id
                    )
                )

            flash("Book added successfully.", "success")
            return redirect(url_for("books.list"))

    return render_template(
        "books/form.html",
        title="Add Book",
        categories=categories
    )


# ---------------------------
# Edit Book (Admin Only)
# ---------------------------
@books_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit(id):
    # Fetch the book from the database by ID
    book = get_book(id)

    # If the book does not exist, show error and redirect
    if book is None:
        flash("Book not found.", "error")
        return redirect(url_for("books.list"))

    # Get all categories for the category dropdown
    categories = get_categories()

    if request.method == "POST":
        # ---------------------------
        # Collect form data
        # ---------------------------
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        published_date = request.form.get("published_date")
        hepburn = request.form.get("hepburn", "").strip()
        release = request.form.get("release", "").strip()
        url = request.form.get("url", "").strip()
        summary = request.form.get("summary", "").strip()
        category_id = int(request.form.get("category_id"))

        # ---------------------------
        # Validate required fields
        # ---------------------------
        if not title:
            flash("Title is required.", "error")
        else:
            # ---------------------------
            # Update the book in the database
            # ---------------------------
            conn = get_db_connection()
            conn.execute(
                """
                UPDATE books
                SET title = ?, author = ?, published_date = ?, hepburn = ?,
                    release = ?, url = ?, summary = ?, category_id = ?
                WHERE id = ?
                """,
                (title, author, published_date, hepburn, release, url, summary, category_id, id)
            )
            conn.commit()
            conn.close()

            # Notify success and redirect to the list
            flash("Book updated successfully.", "success")
            return redirect(url_for("books.list"))

    # ---------------------------
    # Render the edit form template
    # ---------------------------
    return render_template(
        "books/form.html",
        title="Edit Book",
        book=book,
        categories=categories
    )


# ---------------------------
# Delete Book (Admin Only)
# ---------------------------
@books_bp.route("/delete/<int:id>", methods=["POST"])
@admin_required
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Book deleted successfully.", "success")
    return redirect(url_for("books.list"))
