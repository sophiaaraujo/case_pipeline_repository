import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import json


def transform_data():
    with open('/opt/airflow/data_lake/bronze/raw_breweries.json') as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    df.to_parquet('/opt/airflow/data_lake/silver/silver_breweries.parquet', index=False, engine='pyarrow',
                  partition_cols=['state'])


transform_data()
