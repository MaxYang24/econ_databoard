# app.py
from flask import Flask, render_template
import sqlite3
import config

app = Flask(__name__)

def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(config.SQLITE_DB_PATH)
    # Enable dictionary-like row access
    conn.row_factory = sqlite3.Row
    return conn

def get_time_series(country, indicator):
    """Fetch time-series data for a given country and indicator from SQLite."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT date, value
        FROM macro_data
        WHERE country = ? AND indicator = ?
        ORDER BY date ASC
    """, (country, indicator))
    rows = cur.fetchall()
    conn.close()
    # Format data: convert row['date'] and row['value']
    data = [[row['date'], row['value']] for row in rows]
    return data

@app.route('/')
def index():
    return "<h1>Welcome to the Macro Dashboard (SQLite)</h1>"

# app.py (add this route after the index route)

@app.route('/dashboard')
def dashboard():
    # For demonstration, query US inflation data.
    inflation_data = get_time_series('US', 'inflation')
    # print("Inflation Data:", inflation_data)  # For debugging
    return render_template('dashboard.html', inflation_data=inflation_data)

@app.route('/dashboard/eu')
def dashboard_eu():
    eu_inflation_data = get_time_series('EU', 'inflation')
    return render_template('dashboard.html', inflation_data=eu_inflation_data, region='EU')

if __name__ == '__main__':
    app.run(debug=True)
