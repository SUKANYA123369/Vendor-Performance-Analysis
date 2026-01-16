import pandas as pd
import os
import logging
import time
from datetime import datetime
import sqlite3

# ------------------ PATH SETUP ------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
DB_DIR = os.path.join(PROJECT_ROOT, "database")
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "inventory.db")
LOG_PATH = os.path.join(LOG_DIR, "ingestion.log")

# ------------------ LOGGING SETUP ------------------
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ------------------ START TIMING ------------------
start_time = time.time()
start_timestamp = datetime.now()

logging.info("Ingestion process started")
logging.info(f"Start timestamp: {start_timestamp}")

# ------------------ DATABASE CONNECTION ------------------
conn = sqlite3.connect(DB_PATH)

def ingest_db(df, table_name, conn, if_exists):
    df.to_sql(
        table_name,
        con=conn,
        if_exists=if_exists,
        index=False
    )

# ------------------ INGESTION CONFIG ------------------
CHUNK_SIZE = 20000

# ------------------ INGESTION LOOP ------------------
for file in os.listdir(RAW_DATA_DIR):
    if file.endswith(".csv"):
        file_path = os.path.join(RAW_DATA_DIR, file)
        table_name = file.replace(".csv", "")

        logging.info(f"Processing file: {file}")

        try:
            for i, chunk in enumerate(pd.read_csv(file_path, chunksize=CHUNK_SIZE)):
                ingest_db(
                    chunk,
                    table_name,
                    conn,
                    if_exists="replace" if i == 0 else "append"
                )

                logging.info(
                    f"{file} | chunk {i+1} | rows inserted: {chunk.shape[0]}"
                )

        except Exception as e:
            logging.error(f"Error processing {file}: {e}", exc_info=True)

# ------------------ END TIMING ------------------
end_time = time.time()
end_timestamp = datetime.now()

logging.info("Ingestion process completed")
logging.info(f"End timestamp: {end_timestamp}")
logging.info(f"Total execution time: {end_time - start_time:.2f} seconds")

conn.close()

print("✅ Data ingestion completed successfully")
