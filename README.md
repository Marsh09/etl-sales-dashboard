# ETL Project + Flask Dashboard

ETL pipeline in Python that extracts three sources, cleans and merges them, loads a `Sales` table into **SQL Server**, and shows it in a **Flask** dashboard.

| Source | Format |
|---|---|
| `data/customers.csv` | CSV |
| `data/orders.parquet` | Parquet |
| `data/products.csv` | Retrieved from an API (`PRODUCTS_API_URL`); falls back to `data/products_sample.json` |

## Transformations
- **Customers:** remove duplicates (duplicate ids are remapped to the kept id so their orders survive), title-case city, invalid age (outside 18-100) set to null, missing email -> `not_provided`, add `full_name`.
- **Orders:** drop duplicate `order_id`, keep quantity > 0, parse `order_date`, keep only valid `customer_id`.
- **Products:** drop duplicates, standardize product/category text, numeric `unit_price` > 0.
- **Sales:** merge all three; `total_amount = quantity * unit_price`. Columns: `order_id, customer, product, quantity, unit_price, total_amount`.

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env      # set SQL Server details and PRODUCTS_API_URL
python run_etl.py --no-load   # dry run -> output/sales.csv
python run_etl.py             # load into SQL Server (table: Sales)
python dashboard/app.py       # open http://127.0.0.1:5000
```
Requires the Microsoft ODBC Driver for SQL Server and an existing database named in `.env`.

## Structure
```
etl/        config, extract, transform, load
dashboard/  Flask app + HTML template
data/       input files
run_etl.py  pipeline entry point
```
