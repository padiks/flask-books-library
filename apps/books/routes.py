from flask import Blueprint, render_template
from .models import get_all_books

books_bp = Blueprint(
    "books",
    __name__,
    template_folder="templates"
)

# ---------------------------
# List Books
# ---------------------------
@books_bp.route("/")
def list():
    books = get_all_books()
    return render_template("books/list.html", items=books)
