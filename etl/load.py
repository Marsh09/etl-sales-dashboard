import pandas as pd
from sqlalchemy import create_engine
from .config import connection_url

def load_sales(sales: pd.DataFrame, table: str = "Sales") -> None:
    engine = create_engine(connection_url(), fast_executemany=True)
    sales.to_sql(table, engine, if_exists="replace", index=False)
    print(f"Loaded {len(sales)} rows into SQL Server table '{table}'.")
