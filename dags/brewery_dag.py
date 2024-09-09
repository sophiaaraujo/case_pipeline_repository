from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from datetime import datetime
import logging

from scripts.fetch_data import fetch_breweries_data
from scripts.transform_data import transform_breweries_data
from scripts.load_data import load_aggregated_data

# Argumentos padrões do DAG - inclui controle de erros, como envio de email em caso de falha e definição de retries e delay
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Inicia o DAG
dag = DAG(
    'brewery_data_pipeline',
    default_args=default_args,
    description='A DAG to manage brewery data pipeline',
    schedule_interval='@daily',
    start_date=datetime(2024, 9, 1),
    catchup=False,
    tags=['brewery', 'data_pipeline']
)

# Define tarefa inicial
start = DummyOperator(
    task_id='start',
    dag=dag
)

# Define a tarefa final:
end = DummyOperator(
    task_id='end',
    dag=dag
)

# Tarefa para pegar o dado da API:
fetch_task = PythonOperator(
    task_id='fetch_breweries_data',
    python_callable=fetch_breweries_data,
    op_kwargs={'output_file': '/opt/airflow/scripts/raw_breweries.json'},
    provide_context=True,
    dag=dag
)

# Tarefa para a transformação do dado:
transform_task = PythonOperator(
    task_id='transform_breweries_data',
    python_callable=transform_breweries_data,
    op_kwargs={
        'input_file': '/opt/airflow/scripts/raw_breweries.json',
        'output_file': '/opt/airflow/data_lake/silver/silver_breweries.parquet'
    },
    provide_context=True,
    dag=dag
)

# Tarefa para a camada final de visualização
load_task = PythonOperator(
    task_id='load_aggregated_data',
    python_callable=load_aggregated_data,
    op_kwargs={
        'input_file': '/opt/airflow/data_lake/silver/silver_breweries.parquet',
        'output_file': '/opt/airflow/data_lake/gold/gold_breweries.csv'
    },
    provide_context=True,
    dag=dag
)

# Define ordem das tarefas:
start >> fetch_task >> transform_task >> load_task >> end
