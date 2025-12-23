# Flask Books List — Modular & Scalable Architecture

**A modular and scalable Flask web application for managing books and categories**

The repository includes a **sample SQLite database (`db.sqlite3`)** with preloaded tables and test data.

Available login credentials:

* **User account:** `user` / `@User123`
* **Admin account:** `admin` / `root`

You can **check the running project online** at: [https://bukksu.pythonanywhere.com](https://bukksu.pythonanywhere.com) ✅ 

---

## Set up environment & Requirements

```
$ cd project_folder
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install Flask passlib[bcrypt] pandas openpyxl
(venv) $ flask run
```

---

## 📁 Project Structure

```
project_folder/
|
+-- app.py                               # Minimal entry point, calls create_app()
+-- config.py                            # App configuration (settings.py)
|
+-- apps/                                # Modular blueprints (feature-based)
|   +-- categories/
|   |   +-- __init__.py
|   |   +-- routes.py                    # Category views/routes
|   |   +-- templates/categories/
|   |       +-- form.html
|   |       +-- list.html
|   |       +-- view.html
|   |
|   +-- books/
|   |   +-- __init__.py
|   |   +-- routes.py                    # Book views/routes
|   |   +-- models.py                    # DB access helpers / ORM-like functions
|   |   +-- templates/books/
|   |       +-- form.html
|   |       +-- list.html
|   |       +-- view.html
|   |
|   +-- <other-modules>/                 # Future blueprints
|
+-- core/                                # App-wide infrastructure
|   +-- __init__.py                      # Marks core as a Python package
|   +-- app_factory.py                   # create_app() and blueprint registration
|   +-- extensions.py                    # Shared extensions (DB, login, etc.)
|   +-- auth.py                           # Login/logout/session helpers
|   +-- errors.py                         # Global error handlers (404, 500)
|   +-- middleware.py                     # before_request/after_request hooks
|
+-- templates/                            # Project-wide templates
|   +-- base.html                         # Base layout
|   +-- 404.html                          # Global 404 page
|   +-- login.html                        # Global login page
|
+-- static/                               # Static assets
|   +-- css/
|   |   +-- style.css
|
+-- instance/
    +-- db.sqlite3                        # SQLite DB 
```

> ✅ This is a modular, scalable, and Django-like project structure — perfect for small to medium web apps.

---

## Key Principles

### 1️⃣ Blueprints per feature

```text
apps/
  categories/
  books/
```

* Each feature owns its routes, templates, and models.
* Easy to extend, disable, or maintain.

---

### 2️⃣ Application Factory

```text
core/__init__.py   ← create_app()
config.py
```

* Clean startup with environment configurations.
* Enables testing, CLI commands, multiple instances.

---

### 3️⃣ Templates Layout

```
templates/
  404.html
  base.html
  login.html
  includes/   # optional
  app_name/   # optional
```

* Prevents collisions
* Enables reuse
* Matches professional Flask practices

---

### 4️⃣ Explicit Registration

* Nothing hidden.
* All blueprints and routes are registered intentionally.
* Matches preference for clarity and control.

---

### 5️⃣ Database Table Example

```sql
CREATE TABLE "categories" (
	"id"	integer NOT NULL,
	"name"	varchar(255) NOT NULL UNIQUE,
	"description"	text,
	PRIMARY KEY("id" AUTOINCREMENT)
);
```

```sql
CREATE TABLE "books" (
    "id"            INTEGER PRIMARY KEY AUTOINCREMENT,
    "published_date" DATE NOT NULL,
    "title"         VARCHAR(255) NOT NULL,
    "hepburn"       VARCHAR(255) NOT NULL,
    "author"        VARCHAR(255) NOT NULL,
    "release"       VARCHAR(255) NOT NULL,
    "url"           VARCHAR(255) NOT NULL,
    "summary"       TEXT,
    "category_id"   INTEGER NOT NULL,
    FOREIGN KEY("category_id") REFERENCES "categories"("id") DEFERRABLE INITIALLY DEFERRED
);
```

---

### ✅ Why this structure works

* **Modular** — Each feature lives in its own blueprint (`apps/books`, `apps/categories`, etc.), with its own routes, models, and templates. Blueprints can be added or removed independently.
* **Scalable** — The `core/` folder centralizes app-wide infrastructure:

  * `app_factory.py` handles app creation and blueprint registration
  * `auth.py` manages login/logout
  * `middleware.py` enforces global rules like login checks
  * `errors.py` centralizes error handling
  * `extensions.py` provides reusable helpers (DB connection, etc.)
* **Clean app.py** — Minimal entry point, just calls `create_app()`.
* **Maintainable** — Clear separation of concerns between core, modules, templates, and static assets.
* **Future-proof** — Adding new modules, templates, or middleware doesn’t require touching existing modules or `app.py`.
* **Django-like organization** — Familiar structure for long-term projects, making it easy for new developers to understand.

---

## 🧩 Additional Modules

### 1️⃣ Primer Module

* Demonstrates basic Flask features: Blueprints, templates, GET/POST handling, and simple operations.
* Example functionality includes showing messages, calculating sums, and performing operations via form inputs.
* Serves as a **hands-on learning module** for understanding Flask routing and template rendering.

### 2️⃣ Excel Module

* Enables uploading and displaying Excel files (`excel.xlsx`) directly in the browser.
* Uses **Pandas** and **Openpyxl** to read `.xlsx` files.
* Shows the first **10 rows and 6 columns** in a clean HTML table with optional admin-restricted upload functionality.
* Useful for **quickly viewing or managing data online** without needing a separate local Excel client.

> Both modules are **modular and scalable**, following the same blueprint pattern as other apps (`apps/primer` and `apps/excel`) and can be **added or removed independently**.

---

## PythonAnywhere.com — Set Up Environment, Requirements & WSGI

This guide explains how to prepare your Flask project on PythonAnywhere by creating a virtual environment, installing dependencies, and configuring WSGI. Make sure to **use Python 3.11** explicitly.

> **Note:** Your project files should already be uploaded to `/home/bukksu/library`.

```bash
cd ~
python3.11 --version
python3.11 -m venv bukksu-venv
source bukksu-venv/bin/activate
pip install --upgrade pip
pip install Flask passlib[bcrypt] pandas openpyxl
```

### WSGI Setup

1. In the **Web tab**, create a new web app with **manual configuration** and **Python 3.11**.
2. Set the **Virtualenv** path to `/home/bukksu/bukksu-venv`.
3. Edit the WSGI file to point to your project folder and Flask app:

```python
import sys
import os

project_home = '/home/bukksu/library'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from core.app_factory import create_app
application = create_app()
```

4. **Reload** the web app — your Flask application should now be live.

---

## 📄 License

This project is for **learning and educational use**.
Feel free to explore, extend, and build upon it.
