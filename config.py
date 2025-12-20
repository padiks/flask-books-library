import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE = os.path.join(BASE_DIR, "instance", "db.sqlite3")
    SECRET_KEY = "The quick brown fox jumps over the fence."
    # Add other global configs if needed
