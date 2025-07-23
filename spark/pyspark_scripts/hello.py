# Import SparkSession
from pyspark.sql import SparkSession

# Create SparkSession 
spark = SparkSession.builder \
      .master("yarn") \
      .appName("helloworld") \
      .enableHiveSupport() \
      .getOrCreate() 

# Create RDD from external Data source

students =[{'rollno':'001','name':'sravan','age':23,'height':5.79,'weight':67,'address':'guntur'},
               {'rollno':'002','name':'ojaswi','age':16,'height':3.79,'weight':34,'address':'hyd'},
               {'rollno':'003','name':'gnanesh chowdary','age':7,'height':2.79,'weight':17,'address':'patna'},
               {'rollno':'004','name':'rohith','age':9,'height':3.69,'weight':28,'address':'hyd'},
               {'rollno':'005','name':'sridevi','age':37,'height':5.59,'weight':54,'address':'hyd'}]

df = spark.createDataFrame(students)
df.write.csv("/temp/helloworld", sep='\t', header=True, mode='overwrite')
