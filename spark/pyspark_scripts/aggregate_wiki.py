import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import desc, lit
from datetime import datetime, timedelta

def get_args():
    parser = argparse.ArgumentParser(description="PySpark application with date arguments.")
    parser.add_argument("--execution-ts", help="Execution timestamp.")
    execution_ts = parser.parse_args().execution_ts
    print("execution_ts :", execution_ts)
    print("execution_ts type :", type(execution_ts))
    return execution_ts

def parse_args(execution_ts):
    date_str = execution_ts.split('.')[0]
    date_format = "%Y-%m-%dT%H:%M:%S"
    date = datetime.strptime(date_str, date_format) - timedelta(hours=1)
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    print("date :", year, month, day, hour)
    return year, month, day, hour

execution_ts = get_args()
year, month, day, hour = parse_args(execution_ts)

spark = SparkSession.builder \
      .master("yarn") \
      .appName("aggregate_wiki") \
      .config("spark.driver.memory", "1g") \
      .config("spark.driver.cores", "1") \
      .config("spark.executor.memory", "1g") \
      .config("spark.executor.cores", "1") \
      .config("spark.executor.instances", "1") \
      .config("spark.jars.packages", "org.apache.spark:spark-hive_2.12:3.5.5") \
      .enableHiveSupport() \
      .getOrCreate() 

spark.sql("use default")
spark.sql("""create external table if not exists wiki (wiki string, count int)
    partitioned by (timestamp string)
    stored as parquet
    location 'hdfs://hadoop:9000/user/hive/warehouse/wiki'""")

df = spark.read.parquet(f"hdfs://hadoop:9000/datalake/data/wiki/year={year}/month={month}/day={day}/hour={hour}/*.snappy.parquet")
aggregated_df = df.groupBy('wiki').count().sort(desc('count')) \
    .withColumn('timestamp', lit(f"{year:04d}{month:02d}{day:02d}_{hour:02d}")) \
    .limit(10)
aggregated_df.show(truncate=False)
aggregated_df.write.mode("overwrite").saveAsTable('wiki')
