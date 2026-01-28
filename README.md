# 🏦 LanceLoans: Data Pipeline & Setup

## Overview

This project utilizes a **Hybrid Data Pipeline** to efficiently handle loan data from Azure SQL. Instead of querying the cloud database for every analysis session, we implement a **Local Caching Strategy** using the `.parquet` format.

**Key Benefits:**

* **Speed:** Loading from Parquet is ~50x faster than querying SQL over the network.
* **Type Safety:** Unlike CSVs, Parquet preserves data types (Integers stay Integers), eliminating parsing errors.
* **Offline Access:** Analysis can continue without an active internet connection.

---

## 🛠 System Architecture

1. **Source:** Azure SQL Database (Cloud)
2. **Connection:** Python (`SQLAlchemy` + `pyodbc`) via ODBC Driver 17.
3. **Storage:** Local compressed cache (`lance_loans_cache.parquet`).
4. **Analysis:** Pandas loads directly from the local cache.

---

## ⚙️ Installation & Prerequisites

### 1. System Drivers

You must have the **Microsoft ODBC Driver 17 for SQL Server** installed on your machine to talk to Azure.

* **Windows:** Installed by default (usually).
* **Linux/WSL:** Requires `msodbcsql17` (via `apt-get`).
* **Mac:** Requires `msodbcsql17` (via `brew`).

### 2. Python Dependencies

Install the required libraries for connection and Parquet handling:

```bash
pip install pandas sqlalchemy pyodbc python-dotenv pyarrow

```

---

## 🚀 Setup Instructions

### Step 1: Secure Credentials

Create a `.env` file in the root directory. **Do not share this file.**

```ini
DB_SERVER=serverName
DB_NAME=dbName
DB_USER=username
DB_PASSWORD=YourActualPassword

```

### Step 2: The Ingestion Script

We use a reusable Python script (`getdata.py`) to manage data fetching.

* **Logic:** The script checks if `lance_loans_cache.parquet` exists locally.
* **If Yes:** It loads the file instantly.
* **If No:** It connects to Azure, downloads the data, saves the Parquet cache, and *then* returns the dataframe.



### Step 3: Usage in Notebooks

In your EDA notebooks (e.g., `analysis.ipynb`), simply import the function:

```python
from getdata import get_data

# FAST: Loads from local cache (Default)
df = get_data()

# SLOW: Forces a re-download from Azure (Use when DB is updated)
df = get_data(refresh=True)

```

---

## ⚠️ Troubleshooting common errors

| Error | Solution |
| --- | --- |
| `Can't open lib 'ODBC Driver 17'` | You are missing the system driver. Install `msodbcsql17`. |
| `Unable to find a usable engine` | You are missing the Parquet engine. Run `pip install pyarrow`. |
| `Login failed for user` | Check your `.env` file. Ensure `DB_USER` is correct. |
| `Client with IP ... is not allowed` | Go to Azure Portal -> SQL Server -> Networking -> Add your IP to the Firewall. |

---

## 📂 Git Hygiene

The following files are **ignored** in `.gitignore` to maintain security and repo size:

* `.env` (Contains passwords)
* `*.parquet` (Contains large datasets)
* `__pycache__/` (Python build files)