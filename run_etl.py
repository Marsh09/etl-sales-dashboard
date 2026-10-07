"""Run the full pipeline. Use --no-load to skip SQL Server and write output/sales.csv instead."""
import argparse
from pathlib import Path
from etl.extract import extract_customers, extract_orders, extract_products
from etl.transform import clean_customers, clean_orders, clean_products, build_sales

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-load", action="store_true")
    args = ap.parse_args()

    customers, id_map = clean_customers(extract_customers())
    orders = clean_orders(extract_orders(), set(customers["customer_id"]), id_map)
    products = clean_products(extract_products())
    sales = build_sales(customers, orders, products)
    print(sales.to_string(index=False))

    if args.no_load:
        Path("output").mkdir(exist_ok=True)
        sales.to_csv("output/sales.csv", index=False)
        print("Wrote output/sales.csv")
    else:
        from etl.load import load_sales
        load_sales(sales)

if __name__ == "__main__":
    main()
