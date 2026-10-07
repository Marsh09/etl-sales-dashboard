import os
from pathlib import Path
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()
BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"

def connection_url() -> str:
    server = os.getenv("SQL_SERVER", "localhost")
    db = os.getenv("SQL_DATABASE", "SalesDB")
    driver = os.getenv("SQL_DRIVER", "ODBC Driver 17 for SQL Server")
    user, pwd = os.getenv("SQL_USER"), os.getenv("SQL_PASSWORD")
    if user:
        odbc = f"DRIVER={{{driver}}};SERVER={server};DATABASE={db};UID={user};PWD={pwd}"
    else:
        odbc = f"DRIVER={{{driver}}};SERVER={server};DATABASE={db};Trusted_Connection=yes"
    return "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc)
