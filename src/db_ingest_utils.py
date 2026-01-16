import pandas as pd

def ingest_db(df, table_name, engine, if_exists="replace"):
    df.to_sql(
        table_name,
        con=engine,
        if_exists=if_exists,
        index=False
    )
