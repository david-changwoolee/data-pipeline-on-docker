#!/bin/bash

#hadoop entrypoint
service ssh start
hdfs namenode -format -nonInteractive
start-all.sh
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -chown hive:hdfs /user/hive/warehouse
hdfs dfs -chmod 775 /user/hive/warehouse
hdfs dfs -mkdir -p /datalake/data/wiki
hdfs dfs -chown spark:hdfs /datalake/data/wiki
hdfs dfs -chmod 755 /datalake/data/wiki
hdfs dfs -mkdir -p /datalake/checkpoint/wiki
hdfs dfs -chown spark:hdfs /datalake/checkpoint/wiki
hdfs dfs -chmod 755 /datalake/checkpoint/wiki
hdfs dfs -mkdir -p /datawarehouse/data/wiki
hdfs dfs -chown spark:hdfs /datawarehouse/data/wiki
hdfs dfs -chmod 755 /datawarehouse/data/wiki

#hive entrypoint
schematool -dbType mysql -initSchema
#schematool -dbType derby -initSchema
nohup hive --service metastore &> ${HIVE_HOME}/logs/metastore.log &

exec "$@"
