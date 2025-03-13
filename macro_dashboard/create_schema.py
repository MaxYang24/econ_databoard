# create_schema.py
import sqlite3
import config

conn = sqlite3.connect(config.SQLITE_DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS macro_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT,
    indicator TEXT,
    date DATE,
    value REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(country, indicator, date)
)
""")

conn.commit()
conn.close()
print("Database schema created successfully!")
