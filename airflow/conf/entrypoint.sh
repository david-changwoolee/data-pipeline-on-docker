#!/bin/bash

airflow db migrate
airflow users create --username airflow --password airflow --firstname airflow --lastname airflow --role Admin --email david.changwoolee@gmail.com
airflow scheduler -D &
airflow webserver --port 8082
#exec "$@"
