from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.models import Variable


def get_cmds():
    cmds = ['consumer_key=' + str(Variable.get("consumer_key")) + ' consumer_secret=' + str(Variable.get("consumer_secret")) + ' token=' + str(Variable.get("token")) + ' user=' + str(Variable.get("user")) + ' password=' + str(Variable.get("password")), "python3", "cdc-test.py"]
    print(cmds)
    return cmds

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
    image='renannunes/cdc-sf-test',
    # image_pull_policy='Never',
    cmds=get_cmds(),
    labels={"foo": "bar"},
    name="task-1",
    is_delete_operator_pod=True,
    in_cluster=True,
    task_id="task-1",
    # config_file=os.path.expanduser('~')+"/.kube/config",
    get_logs=True,
    dag=dag
)

task

