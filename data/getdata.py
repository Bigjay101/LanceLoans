import pandas as pd
import os
import urllib
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Setup connection (as discussed before)
load_dotenv()
server = os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
# driver = '{ODBC Driver 17 for SQL Server}'
driver = '{ODBC Driver 18 for SQL Server}'

conn_str = (
    "mssql+pyodbc:///?odbc_connect="
    + urllib.parse.quote_plus(
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
)


engine = create_engine(conn_str)

# conn_str = f'mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}")}'
# engine = create_engine(conn_str)

CACHE_FILE = "lance_loans_cache.parquet"

def get_data(refresh=False):
    """
    Loads data from local cache if it exists. 
    Otherwise, pulls from Azure and creates the cache.
    """
    if os.path.exists(CACHE_FILE) and not refresh:
        print("⚡ Loading from local cache (Fast)...")
        return pd.read_parquet(CACHE_FILE)
    
    else:
        print("☁️  Downloading fresh data from Azure SQL...")
        query = "SELECT * FROM data_raw"
        df = pd.read_sql(query, engine)
        
        # Save to Parquet to speed up next time
        df.to_parquet(CACHE_FILE)
        print(f"✅ Data saved to {CACHE_FILE}")
        return df

# --- USAGE ---

# Day-to-day work (Instant load):
df = get_data() 
# When you know new data was added to the DB:
# df = get_data(refresh=True)