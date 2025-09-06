#!/bin/bash

#spark entrypoint

start-thriftserver.sh --hiveconf hive.server2.thrift.bind.host=spark
jupyter notebook --allow-root --port 9000 --ip 0.0.0.0

exec "$@"
