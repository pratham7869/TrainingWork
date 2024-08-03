from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

conf = SparkConf().setAppName("MyApp")
sc = SparkContext(conf=conf)
ui_url = sc.uiWebUrl
print(f"Spark UI is running at: {ui_url}")
spark = SparkSession.builder.appName("testpyspark").getOrCreate()
print("print the spark object")
print(spark)

# Read the CSV file
df = spark.read.csv("C:\githubrepo\TrainingWork\SparkPractice\gods.csv", header=True, inferSchema=True)

# Showing the DataFrame
df.show()

# Print the schema of the DataFrame
df.printSchema()

row_count = df.count()
print(row_count)
# Stop the SparkSession
print(input("press enter"))
spark.stop()



