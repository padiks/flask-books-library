import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
import pandas as pd
from core.auth import admin_required # Decorator @admin_required coming from core/auth.py

# Define a Blueprint for the module
excel_bp = Blueprint(
    "excel",  # Blueprint name
    __name__,  # Current module (helps with finding files)
    template_folder="templates"  # Folder for templates
)


# ---------------------------
# Absolute paths for PythonAnywhere
# ---------------------------
# PROJECT_HOME = '/home/bukksu/library'           # Your project folder
# UPLOAD_FOLDER = os.path.join(PROJECT_HOME, 'uploads')  # Absolute path to uploads
# EXCEL_FILE = os.path.join(UPLOAD_FOLDER, 'excel.xlsx')  # Absolute path to excel.xlsx


# ---------------------------
# Relative paths for local testing
# ---------------------------
UPLOAD_FOLDER = 'uploads/'
EXCEL_FILE = os.path.join(UPLOAD_FOLDER, 'excel.xlsx')  # File path for excel.xlsx


# ---------------------------
# Route for the Blueprint View
# ---------------------------
@excel_bp.route("/", methods=["GET", "POST"])  # Accept GET and POST requests
def list():
    """
    Handles the request to upload or view the excel file.
    If no file is uploaded, it reads 'excel.xlsx' from the 'uploads/' directory.
    Only the first 10 rows and first 6 columns are displayed.
    """

    excel_data = None
    excel_columns = None

    # ---------------------------
    # Handle file upload via POST request (admin only)
    # ---------------------------
    if request.method == "POST":
        return _handle_upload()  # Delegate to separate function

    # ---------------------------
    # Display existing Excel file
    # ---------------------------
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE, header=None)

        # Slice the DataFrame: first 10 rows, first 6 columns
        df = df.iloc[:10, :6]

        # Generate generic column names (Col 1, Col 2, ...)
        excel_columns = [f"Col {i+1}" for i in range(df.shape[1])]
        excel_data = df.values.tolist()

    # Render the template and pass the data
    return render_template("excel/list.html", excel_columns=excel_columns, excel_data=excel_data)


# ---------------------------
# Admin-only Upload Handler
# ---------------------------
@admin_required
def _handle_upload():
    """
    Handles the Excel file upload.
    Only accessible by admin users.
    """
    file = request.files.get('file')
    if file and file.filename == 'excel.xlsx':
        # Save the uploaded file
        file.save(EXCEL_FILE)
        flash("File uploaded successfully! Redirecting to reload the page.")  # Show a temporary message
    else:
        flash("No valid file uploaded.")

    return redirect(url_for('excel.list'))
