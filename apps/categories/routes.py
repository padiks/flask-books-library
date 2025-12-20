import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

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
# Add Category
# ---------------------------
@categories_bp.route("/add", methods=["GET", "POST"])
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
# Edit Category
# ---------------------------
@categories_bp.route("/edit/<int:id>", methods=["GET", "POST"])
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
# Delete Category
# ---------------------------
@categories_bp.route("/delete/<int:id>", methods=["POST", "GET"])
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
    # For GET request, we could render a simple confirmation template or just delete directly
    return render_template("categories/view.html", category=category, title="Delete Category")
