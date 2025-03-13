# ingest/fetch_ecb.py
import sqlite3
import config
import requests
import json

def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(config.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_and_store_eu_inflation():
    """
    Fetch European inflation data (HICP) from the ECB SDW API and store it in the SQLite database.
    This example assumes the ECB provides a JSON response with a known structure.
    """
    # ECB SDW URL for HICP data (this is an example URL; adjust if needed)
    url = "https://sdw-wsrest.ecb.europa.eu/service/data/ICP/M.U2.N.000000.4.ANR?detail=dataonly"
    headers = {'Accept': 'application/json'}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error fetching ECB data:", response.status_code)
        return

    data = response.json()
    
    # Example parsing logic:
    try:
        # Access the series data. The actual keys might differ; adjust as necessary.
        series = data['dataSets'][0]['series']
        # Access the dimension information for observation period (assume first observation dimension is time)
        time_values = data['structure']['dimensions']['observation'][0]['values']
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Iterate over the series (keys are strings representing series attributes)
        for series_key, series_data in series.items():
            observations = series_data['observations']
            for obs_key, obs_value in observations.items():
                # obs_key is a string like "0:0:0:0". The first part represents the index in time_values.
                time_index = int(obs_key.split(':')[0])
                period_id = time_values[time_index]['id']  # e.g., "2020-01"
                # Convert period to a date string (assume first day of month)
                date_str = period_id + "-01"
                value = obs_value[0]  # The observed value

                cur.execute("""
                    INSERT OR IGNORE INTO macro_data (country, indicator, date, value)
                    VALUES (?, ?, ?, ?)
                """, ('EU', 'inflation', date_str, value))
        
        conn.commit()
        cur.close()
        conn.close()
        print("EU Inflation data fetched and stored successfully.")
    except Exception as e:
        print("Error parsing ECB data:", e)

if __name__ == '__main__':
    fetch_and_store_eu_inflation()
