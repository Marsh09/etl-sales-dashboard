import numpy as np
import pandas as pd

def clean_customers(df: pd.DataFrame):
    """Returns (clean customers, id_map) where id_map sends duplicate ids to the kept id."""
    df = df.copy()
    for c in ["first_name", "last_name", "city", "email"]:
        df[c] = df[c].astype("string").str.strip()
    df["city"] = df["city"].str.title()                      # standardize city
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df.loc[~df["age"].between(18, 100), "age"] = np.nan      # validate age (18-100)
    df["email"] = df["email"].str.lower().fillna("not_provided")
    df["full_name"] = df["first_name"] + " " + df["last_name"]

    key = ["first_name", "last_name", "city", "age", "email"]
    first_id = df.groupby(key, dropna=False)["customer_id"].transform("min")
    id_map = dict(zip(df["customer_id"], first_id))
    df = df.drop_duplicates(subset=key).reset_index(drop=True)  # remove duplicates
    return df, id_map

def clean_orders(df: pd.DataFrame, valid_ids, id_map) -> pd.DataFrame:
    df = df.drop_duplicates(subset="order_id").copy()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df = df[df["quantity"] > 0]
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])
    df["customer_id"] = df["customer_id"].map(id_map).fillna(df["customer_id"]).astype(int)
    return df[df["customer_id"].isin(valid_ids)]

def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["product_name"] = df["product_name"].astype(str).str.strip().str.title()
    df["category"] = df["category"].astype(str).str.strip().str.title()
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df[df["unit_price"] > 0]                              # validate price
    return df.drop_duplicates(subset="product_id")

def build_sales(customers, orders, products) -> pd.DataFrame:
    sales = (orders.merge(customers, on="customer_id", how="inner")
                   .merge(products, on="product_id", how="inner"))
    sales["total_amount"] = sales["quantity"] * sales["unit_price"]
    sales = sales.rename(columns={"full_name": "customer", "product_name": "product"})
    return sales[["order_id", "customer", "product", "quantity", "unit_price", "total_amount"]]
