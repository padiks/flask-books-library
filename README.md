# Flask Books List — Modular & Scalable Architecture

**A modular and scalable Flask web application for managing books and categories**

The repository includes a **sample SQLite database (`db.sqlite3`)** with preloaded tables and test data.

Available login credentials:

* **User account:** `user` / `@User123`
* **Admin account:** `admin` / `root`

---

## Set up enviroment & Requirements

```
$ cd project_folder
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install Flask passlib[bcrypt]
(venv) $ flask run
```

---

## 📁 Project Structure

```
project_folder/
|
+-- app.py                               # Entry point (like manage.py)
+-- config.py                            # App configuration (settings.py)
|
+-- apps/                                # Modular blueprints (feature-based)
|   +-- categories/
|   |   +-- __init__.py
|   |   +-- routes.py                    # Views
|   |   +-- templates/categories/
|   |       +-- form.html
|   |       +-- list.html
|   |       +-- view.html
|   |
|   +-- books/
|   |   +-- __init__.py
|   |   +-- routes.py
|   |   +-- models.py
|   |   +-- forms.py
|   |   +-- templates/books/
|   |       +-- form.html
|   |       +-- list.html
|   |       +-- view.html
|   |
|   +-- <other-modules>/                 # Future blueprints
|
+-- templates/                            # Project-wide templates
|   +-- base.html
|   +-- 404.html
|
+-- static/                               # Static assets
|   +-- css/
|   |   +-- style.css
|
+-- instance/
    +-- db.sqlite3                        # SQLite DB (kept out of git)
```

> ✅ This is a modular, scalable, and Django-like project structure — perfect for small to medium Flask web apps.

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
  base.html
  includes/
  app_name/
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

* Modular design — each feature isolated
* Scalable — easy to add new modules
* Maintainable — clear separation of concerns
* Django-like organization — familiar for long-term projects
* Future-proof — can add DB, authentication, and more

Got it! Here's the updated description with your requested setup:

---

## Pythonanywhere.com / Set up Environment & Requirements

To set up your Flask project on PythonAnywhere, follow these steps to create a virtual environment, install dependencies, and upload your project files. Note that WSGI setup is **not included** in this guide.

```
cd ~
python3.13 -m venv books-venv
source books-venv/bin/activate
pip install --upgrade pip
pip install Flask passlib[bcrypt]
```

---

## 📄 License

This project is for **learning and educational use**.
Feel free to explore, extend, and build upon it.

