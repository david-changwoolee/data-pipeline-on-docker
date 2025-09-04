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

**Architecture**

**Data Flow**
1. Airflow dag gets stream data from wikimedia and stores into kafka
   - airflow dag : stream_wiki.py
   - kafka topic : 'wiki'
2. PySpark reads data from kafka and stores into HDFS
   - jupyter notebook name : kafka_streaming.ipynb
   - HDFS write path : /datalake/data/wiki
3. PySpark reads data from HDFS, transforms, and stores into hive table.
   - airflow dag : aggregate_wiki.py
   - pyspark name : aggregate_wiki.py
   - hive table : default.wiki
   - hive location : /datawarehouse/data/wiki

**docker commands**
- docker compose up -d : launch all components
- docker compose up -d <hadoop spark> : launch only hadoop and spark components
- docker volume ls : list docker volume
- docker volume rm <data-pipeline-on-docker_hadoop_config> : remove docker volume named data-pipeline-on-docker_hadoop_config


**What I have learnt**

**To Do**
- Implement HA
- Add test codes
- Add Dashboard

**References**
- apache/kafka official image : https://hub.docker.com/r/apache/kafka
- mysql official image : https://hub.docker.com/_/mysql
- wiki openAPI : https://stream.wikimedia.org/v2/ui/#/?streams=mediawiki.recentchange

