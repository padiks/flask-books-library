import sqlite3
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session, abort

categories_bp = Blueprint(
    "categories",
    __name__,
    template_folder="templates"
)

def get_db_connection():
    db_path = current_app.config["DATABASE"]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # dict-like access
    return conn

# ---------------------------
# Admin Required Decorator
# ---------------------------
def admin_required(f):
    """
    Decorator to protect routes that should only be accessible by the admin user.
    If a non-admin tries to access, it returns a 403 Forbidden error.
    Usage: add @admin_required above your route definition.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") != "admin":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------
# List Categories
# ---------------------------
@categories_bp.route("/")
def list():
    conn = get_db_connection()
    items = conn.execute("SELECT id, name, description FROM categories ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("categories/list.html", items=items)

# ---------------------------
# View Category
# ---------------------------
@categories_bp.route("/view/<int:id>")
def view(id):
    conn = get_db_connection()
    category = conn.execute("SELECT * FROM categories WHERE id = ?", (id,)).fetchone()
    conn.close()

    if category is None:
        flash("Category not found.", "error")
        return redirect(url_for("categories.list"))

    return render_template("categories/view.html", category=category, title="Category Details")

# ---------------------------
# Add Category (Admin Only)
# ---------------------------
@categories_bp.route("/add", methods=["GET", "POST"])
@admin_required  # Only admin can add categories
def add():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("Name is required.", "error")
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO categories (name, description) VALUES (?, ?)", (name, description))
            conn.commit()
            conn.close()
            flash("Category added successfully.", "success")
            return redirect(url_for("categories.list"))

    return render_template("categories/form.html", title="Add Category")


# ---------------------------
# Edit Category (Admin Only)
# ---------------------------
@categories_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@admin_required  # Only admin can edit categories
def edit(id):
    conn = get_db_connection()
    category = conn.execute("SELECT * FROM categories WHERE id = ?", (id,)).fetchone()

    if category is None:
        conn.close()
        flash("Category not found.", "error")
        return redirect(url_for("categories.list"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("Name is required.", "error")
        else:
            conn.execute("UPDATE categories SET name = ?, description = ? WHERE id = ?", (name, description, id))
            conn.commit()
            conn.close()
            flash("Category updated successfully.", "success")
            return redirect(url_for("categories.list"))

    conn.close()
    return render_template("categories/form.html", title="Edit Category", category=category)

# ---------------------------
# Delete Category (Admin Only)
# ---------------------------
@categories_bp.route("/delete/<int:id>", methods=["POST", "GET"])
@admin_required  # <-- Only admin can delete categories
def delete(id):
    conn = get_db_connection()
    category = conn.execute("SELECT * FROM categories WHERE id = ?", (id,)).fetchone()

    if category is None:
        conn.close()
        flash("Category not found.", "error")
        return redirect(url_for("categories.list"))

    if request.method == "POST":
        conn.execute("DELETE FROM categories WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        flash("Category deleted successfully.", "success")
        return redirect(url_for("categories.list"))

    conn.close()
    # For GET request, we could render a simple confirmation template
    return render_template("categories/view.html", category=category, title="Delete Category")
