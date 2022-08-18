from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from google.cloud import bigquery


def main():
    print('Test')
    print(datetime(2022, 7, 1))
    client = bigquery.Client()
    print(client.project)



default_args = {
    'owner': 'Raw',
    'start_date': datetime(2022, 7, 1)
}

with DAG('test', schedule_interval='*/10 * * * *', default_args=default_args) as dag:
    task_1 = PythonOperator(task_id='task_1', python_callable=main)
    