import pandas as pd
import sqlite3
import os

# Paths
DB_PATH = "database/inventory.db"
OUTPUT_DIR = "data/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Connect to DB
conn = sqlite3.connect(DB_PATH)

# Tables to export
tables = ["vendor_sales_summary"]

for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    output_path = os.path.join(OUTPUT_DIR, f"{table}.csv")
    df.to_csv(output_path, index=False)
    print(f"Exported {table} to {output_path}")

conn.close()
