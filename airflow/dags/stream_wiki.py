import logging
import sys
from pprint import pprint

import pendulum

from airflow.models.dag import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import (
        PythonOperator, 
        PythonVirtualenvOperator, 
        is_venv_installed
        )

log = logging.getLogger(__name__)

PATH_TO_PYTHON_BINARY = sys.executable


with DAG(
    dag_id="stream_wiki",
    schedule='* * * * *',
    start_date=pendulum.datetime(2025, 8, 1, tz=pendulum.timezone("Asia/Seoul")),
    catchup=False,
    tags=["wiki"],
):

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    def print_context(ds=None, **kwargs):
        print("::group::All kwargs")
        pprint(kwargs)
        print("::endgroup::")
        print("::group::Context variable ds")
        print(ds)
        print("::endgroup::")
        return "Whatever you return gets printed in the logs"

    print_context = PythonOperator(task_id="print_context", python_callable=print_context)

    if not is_venv_installed():
        log.warning("The virtalenv_python example task requires virtualenv, please install it.")
    else:

        def callable_stream_wiki():
            import re
            import time
            import json
            from pprint import pprint
            import requests
            import sseclient
            from kafka import KafkaProducer

            kafka_bootstrap_servers = ['kafka:9092']
            kafka_topic = 'wiki'

            producer = KafkaProducer(
                    bootstrap_servers = kafka_bootstrap_servers,
                    value_serializer = lambda v: json.dumps(v).encode('utf-8')
                    )
            
            start_time = time.time()
            duration = 50 
            url = 'https://stream.wikimedia.org/v2/stream/mediawiki.recentchange'
            headers = {'Accept': 'text/event-stream'}
            
            response = requests.get(url, stream=True, headers=headers)
            client = sseclient.SSEClient(response)

            for _ in client.events():
                data = json.loads(_.data)
                domain = data.get('meta').get('domain')
                p = re.compile('^[a-z]+.wikipedia.org$')
                if p.match(domain) is not None:
                    message = {'id' : data.get('id'),
                               'wiki' : data.get('wiki'),
                               'timestamp' : data.get('timestamp'),
                               'bot' : data.get('bot')}
                    
                    future = producer.send(kafka_topic, value=message)
                    try:
                        record_metadata = future.get(timeout=5)
                        pprint(f"Successfully sent message to partition {record_metadata.partition} at offset {record_metadata.offset}")
                    except Exception as e:
                        pprint(f"Failed to send message: {e}")
                    
                if time.time() - start_time > duration:
                    break

            producer.flush()
            producer.close()
            pprint("Producer finished.")

        stream_wiki = PythonVirtualenvOperator(
            task_id="stream_wiki",
            python_callable=callable_stream_wiki,
            requirements=["sseclient-py", "requests", "kafka-python"],
            system_site_packages=False,
        )

        start >> print_context >> stream_wiki >> end
