
"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](https://airflow.apache.org/tutorial.html)
"""
# [START tutorial]
# [START import_module]
from datetime import datetime, timedelta
import pendulum

from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator

# [END import_module]

# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
# [END default_args]

# [START instantiate_dag]
with DAG(
    'qqq_analyzer',
    default_args=default_args,
    description='analyze',
    schedule_interval=timedelta(days=1),
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=['airflow'],
) as dag:
    # [END instantiate_dag]

   spark_job = SparkSubmitOperator(
        task_id="example",
        application="/opt/airflow/pyspark_scripts/hello.py",  # DAG 컨테이너 내부 경로
        conn_id="spark",  # Airflow의 Spark connection 설정 (Airflow UI > Admin > Connections)
        conf={"spark.master": "spark://spark:7077"},  # docker-compose 의 서비스 이름으로 Spark master 접근
        verbose=True
    )
