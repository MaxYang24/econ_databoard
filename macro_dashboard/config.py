# config.py
import os

# SQLite configuration: the database file will be "macro.db" in the project root.
SQLITE_DB_PATH = os.environ.get("SQLITE_DB_PATH", "macro.db")
FRED_API_KEY = os.environ.get("FRED_API_KEY", "9f1ac54e163cd78026f568ef34b76fe2")  # Replace with your actual FRED API key
