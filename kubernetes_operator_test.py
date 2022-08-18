from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.models import Variable


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
    namespace='airflow',
    # service_account_name='',
    image='renannunes/cdc-sf-test:latest',
    # image_pull_policy='Never',
    cmds=["python3", "cdc-test.py"],
    env_vars={'consumer_key': Variable.get("consumer_key"),
      'consumer_secret': Variable.get("consumer_secret"),
      'token': Variable.get("token"),
      'user': Variable.get("user"),
      'password': Variable.get("password")
    },
    name="task-1",
    is_delete_operator_pod=True,
    in_cluster=True,
    task_id="task-1",
    # config_file=os.path.expanduser('~')+"/.kube/config",
    get_logs=True,
    dag=dag
)

task

