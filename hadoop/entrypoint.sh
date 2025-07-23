#!/bin/bash

#hadoop entrypoint
service ssh start
hdfs namenode -format -nonInteractive
start-all.sh
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -chown hive:hdfs /user/hive/warehouse
hdfs dfs -chmod 775 /user/hive/warehouse

#hive entrypoint
#schematool -dbType mysql -initSchema
schematool -dbType derby -initSchema
nohup hive --service metastore &> ${HIVE_HOME}/logs/metastore.log &

exec "$@"
