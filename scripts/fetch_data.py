import requests
import json


def fetch_data():
    url = 'https://api.openbrewerydb.org/breweries'
    response = requests.get(url)
    data = response.json()

    with open('/opt/airflow/data_lake/bronze/raw_breweries.json', 'w') as f:
        json.dump(data, f)


fetch_data()
