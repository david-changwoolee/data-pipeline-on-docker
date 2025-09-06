# data-pipeline-on-docker

**Project Goal**
- Create a data pipeline cluster for a testing or staging env prior to prod deployment
- Gain hands-on experience building data pipeline using key systems such as Hadoop, Spark, Hive, Airflow, Kafka, Docker

**Core Systems**
- Docker : docker v28.1.1, docker compose v2.35.1
- Hadoop : hadoop v3.4.1 as 'hadoop' custom image based on Ubuntu 
- Hive : hive v3.1.3 as 'hadoop' custom image
- Spark : spark v3.5.5 as 'spark' custom image based on Ubuntu
- Airflow : airflow v2.11.0 as 'airflow' custom image based on Ubuntu
- Kafka : kafka v4.0.0 as ['apache/kafka' official image](https://hub.docker.com/r/apache/kafka)
- MySql : mysql v9.2.0 as ['mysql' official image](https://hub.docker.com/_/mysql) used as Hive Metastore 

**localhost webui**
- resource manager : localhost:8088
- namenode info : localhost:9870
- datanode info : localhost:9864
- spark history server : localhost:18080
- airflow : localhost:8082
- jupyter notebook : localhost:9000
- metabase graph : localhost:3000

**Data Flow**
1. Airflow dag gets stream data from wikimedia and stores into kafka
   - airflow dag : stream_wiki.py
   - kafka topic : 'wiki'
   - what stream_wiki.py does : reads ['recentchange'(updated content in real time) from wikimedia](https://stream.wikimedia.org/v2/ui/#/?streams=mediawiki.recentchange), filters to get only wiki page update data and stores into kafka 'wiki' topic
2. PySpark reads data from kafka and stores into HDFS
   - jupyter notebook name : kafka_streaming.ipynb
   - HDFS write path : /datalake/data/wiki
3. PySpark reads data from HDFS, transforms, and stores into hive table.
   - airflow dag : aggregate_wiki.py
   - pyspark name : aggregate_wiki.py
   - hive table : default.wiki
   - hive location : /datawarehouse/data/wiki
   - what aggregate_wiki.py does : aggregates to show top 10 wiki page languages by number of wiki page updates
4. Metabase generates graph
   - setup
   - graph

**docker commands**
- docker compose up -d : launch all services
- docker compose up -d hadoop spark : launch only 'hadoop' and 'spark' services
- docker volume ls : list docker volume
- docker volume rm <data-pipeline-on-docker_hadoop_config> : remove docker volume named data-pipeline-on-docker_hadoop_config

**To Do**
- Implement HA
- Add test codes

**References**
- apache/kafka official image : https://hub.docker.com/r/apache/kafka
- mysql official image : https://hub.docker.com/_/mysql
- wiki openAPI : https://stream.wikimedia.org/v2/ui/#/?streams=mediawiki.recentchange
