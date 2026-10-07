import json, os
import pandas as pd
import requests
from .config import DATA

def extract_customers() -> pd.DataFrame:
    return pd.read_csv(DATA / "customers.csv")

def extract_orders() -> pd.DataFrame:
    return pd.read_parquet(DATA / "orders.parquet")

def extract_products() -> pd.DataFrame:
    """Fetch products from an API (PRODUCTS_API_URL); fall back to the bundled sample."""
    url = os.getenv("PRODUCTS_API_URL")
    if url:
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            df = pd.DataFrame(r.json())
        except Exception as e:
            print(f"[warn] API failed ({e}); using data/products_sample.json")
            df = pd.DataFrame(json.loads((DATA / "products_sample.json").read_text()))
    else:
        print("[info] PRODUCTS_API_URL not set; using data/products_sample.json")
        df = pd.DataFrame(json.loads((DATA / "products_sample.json").read_text()))
    df.to_csv(DATA / "products.csv", index=False)  # products.csv as in the spec
    return df
