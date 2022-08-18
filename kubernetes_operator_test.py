from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(year=2022, month=8, day=14),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('kubpodop_test_salesforce',
          schedule_interval='*/30 * * * *',
          catchup=False,
          default_args=default_args,
          tags=['test'])

task = KubernetesPodOperator(
    namespace='default',
    # service_account_name='',
    image='python:3.7',
    # image_pull_policy='Never',
    cmds=["python", "-c", "print('Hello world!')"],
    labels={"foo": "bar"},
    name="task-1",
    is_delete_operator_pod=True,
    in_cluster=False,
    task_id="task-1",
    # config_file=os.path.expanduser('~')+"/.kube/config",
    get_logs=True,
    dag=dag
)

task