import pandas as pd
import pyarrow.parquet as pq


def load_data():
    df = pd.read_parquet('/opt/airflow/data_lake/silver/silver_breweries.parquet')

    # Agregação na última camada, Gold
    aggregated = df.groupby(['brewery_type', 'state']).size().reset_index(name='count')
    aggregated.to_csv('/opt/airflow/data_lake/gold/gold_breweries.csv', index=False)


load_data()
