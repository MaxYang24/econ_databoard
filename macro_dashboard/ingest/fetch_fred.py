# ingest/fetch_fred.py
import sqlite3
from fredapi import Fred
import config

def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(config.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_and_store_inflation():
    """Fetch US inflation data from FRED and store in SQLite."""
    fred = Fred(api_key=config.FRED_API_KEY)
    
    # Fetch CPI data; CPIAUCSL is the Consumer Price Index for All Urban Consumers.
    # This returns a pandas Series with a datetime index.
    data_series = fred.get_series('CPIAUCSL')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Loop through each data point and insert into the database.
    for date, value in data_series.items():
        date_str = date.strftime('%Y-%m-%d')
        try:
            cur.execute("""
                INSERT OR IGNORE INTO macro_data (country, indicator, date, value)
                VALUES (?, ?, ?, ?)
            """, ('US', 'inflation', date_str, value))
        except Exception as e:
            print(f"Error inserting data for {date_str}: {e}")
    
    conn.commit()
    conn.close()
    print("US Inflation data fetched and stored successfully.")

if __name__ == '__main__':
    fetch_and_store_inflation()
