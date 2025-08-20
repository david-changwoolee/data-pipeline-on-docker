from datetime import datetime, timedelta
import pendulum

from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'aggregate_wiki',
    default_args=default_args,
    description='aggregate_wiki',
    schedule_interval=None,
    start_date=pendulum.datetime(2025, 8, 1, tz="UTC"),
    catchup=False,
    tags=['wiki'],
) as dag:

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    spark_job = SparkSubmitOperator(
        task_id="aggregate_wiki",
        name="aggregate_wiki",
        application="/opt/airflow/pyspark_scripts/aggregate_wiki.py",  # DAG 컨테이너 내부 경로
        deploy_mode="cluster",
        conn_id="spark",  # Airflow의 Spark connection 설정 (Airflow UI > Admin > Connections)
        application_args=["--execution-ts", "{{ ts }}"],
        verbose=True
    )

    start >> spark_job >> end
